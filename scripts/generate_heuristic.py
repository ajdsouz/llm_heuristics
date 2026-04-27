from textwrap import indent
import dataclasses
from xml.dom import NotFoundErr # where did this come from?
import os
import json
from dataclasses import dataclass, asdict
import logging 
import click
from src.utils import timer
from src.llm_heuristics import models
from src.llm_heuristics.suites import SUITES, DomainSuite
from src.llm_heuristics.prompt import create_prompt


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s :: %(message)s",
)
logger = logging.getLogger(__name__)


def validate_heuristic_name(ctx, param, value):
    if not value.endswith("Heuristic"):
        raise click.BadParameter("The heuristic name must end with 'Heuristic'.")
    return value


def validate_heuristic_file(ctx, param, value):
    if not value.endswith(".py"):
        raise click.BadParameter("The heuristic name must end with '.py'.")
    return value


def validate_temperature(ctx, param, value):
    if value > 2 or value < 0:
        raise click.BadParameter("The temperature must be in the interval [0,2].")
    return value

def validate_top_p(ctx, param, value):
    if value > 1 or value < 0:
        raise click.BadParameter("The top-P must be in the interval [0,1].")
    return value


@click.command()

@click.option(
    "--base_path",
    "-b",
    help="Base path to the data directory",
)

@click.option(
    "--log_path",
    help="Directory to write logs to",
)
@click.option(
    "--domain",
    "-d",
    required=True,
    type=click.Choice(SUITES.keys()),
    help="Name of the domain used. Everything else is inferred.",
)
@click.option(
    "--problem_dir",
    "-p_dir",
    required=True,
    help="The directory of problem instances. ",
)
@click.option(
    "--instance1",
    "-i1",
    required=True,
    help="First problem file to use to build prompt. Preferable the smmallest problem instance.",
)

@click.option(
    "--instance2",
    "-i2",
    required=True,
    help="Second problem file to use to build prompt. Preferably the longest proble instance.",
)

@click.option(
    "--framework",
    default="gemini",
    type=click.Choice(["gemini", "deepseek", "openai", "local"]),
    help="Framework used to run LLMs.",
)
@click.option(
    "--model",
    "-m",
    default="gemini-2.0-flash-thinking",
    help="LLM Model used. If a local model is used, provide path to local model. The folder should have structure similar to a HF model repo",
)
@click.option(
    "--heuristic-name",
    "-n",
    default="NewDomainDependentHeuristic",
    callback=validate_heuristic_name,
    help="Name of the heuristic and of its class. Name must end with 'Heuristic'. \
    NOTE: This impacts how you will call it from pyperplan!",
)
@click.option(
    "--heuristic-file",
    "-f",
    default="new-heuristic.py",
    callback=validate_heuristic_file,
    help="File where the learnt heuristic is stored. It must be a Python file.",
)
@click.option(
    "--prompt-format",
    default="neurips",
    type=click.Choice(["base", "checklist", "goalcount", "new", "pyperplan", "reordered", "neurips"]),
    help="Format of the prompt passed to the heuristic.",
)
@click.option(
    "--temperature",
    "-t",
    default=1.0,
    type=float,
    callback=validate_temperature,
    help="Model temperature.",
)
@click.option(
    "--top-p",
    default=0.5,
    type=float,
    callback=validate_top_p,
    help="Model top-P.",
)
@click.option(
    "--ablation",
    default="false",
    type=click.Choice(["false", "complete", "description_simple", "domain", "instances", "dependent-heuristics", "state-representation", "static-representation",
                       "planner-code", "checklist", "checklist-no6", "independent-heuristics", "heuristics-nocomment", "dependent-heuristics-and-plans"]),
    help="Ablation options for reordered prompt.",
)

@dataclass
class ExperimentConfig:
    model_name: str
    domain: str
    instance1: str
    instance2: str
    temperature: float
    top_p: float
    generated_heuristic: str
    # runtime_dict: dict
    heuristic_generation_runtime: float # should it be float?

    
@timer
def main(base_path, log_path, domain, problem_dir, instance1, instance2, model, framework, heuristic_name, heuristic_file, prompt_format, temperature, top_p, ablation):
    logging.info(f"Python version: {sys.version}.")
    logging.info(f"Using suite {domain}.")
    # suite = SUITES[domain]
    # if base_path is not None and domain not in SUITES:
    
    domain_data_folder: str = f"{base_path}/{domain}"
    suite = DomainSuite(
        name=domain, 
        domain=f"{domain_data_folder}/domain.pddl",
        instance1=f"{domain_data_folder}/{problem_dir}/{instance1}.pddl",
        instance2=f"{domain_data_folder}/{problem_dir}/{instance2}.pddl",
        state=f"{domain_data_folder}/example-state.out",
        static=f"{domain_data_folder}/example-static.out"
    )
    # elif base_path is None and domain not in SUITES:
    #     raise NotFoundErr("Domain not found in provided Suites and no base_path is provided."
    #     "Provide a valid base_path for unseen domains")
    # else:
    #     suite: DomainSuite = SUITES[domain]
    
    logging.info(f"Using model {model}.")
    logging.info(f"Using temperature {temperature}.")
    logging.info(f"Using top-P {top_p}.")
    logging.info(f"Using ablation option {ablation}")
    logging.info(f"Generating prompt with format {prompt_format}")
    prompt, prompt_creation_time = create_prompt(suite, heuristic_name, prompt_format, ablation)
    logging.info(f"Time to generate prompt: {prompt_creation_time}")
    logging.info("Final prompt: ")
    print(prompt)

    logging.info(f"Using model {model} with framework {framework}.")

    if framework == "gemini":
        answer, model_response_time = models.run_gemini(model, prompt, temperature, top_p)
    elif framework == "deepseek":
        answer, model_response_time = models.run_deepseek(model, prompt, temperature, top_p)
    elif framework == "openai":
        answer, model_response_time = models.run_openai(model, prompt, temperature, top_p)
    elif framework == "local":
        answer, model_response_time = models.run_local(model, prompt, temperature, top_p)

    logging.info("LLM Answer:")
    print(answer)
    logging.info(f"LLM Answer generation time: {model_response_time}")
    if not answer:
        logging.error("LLM returned an empty string!")
        raise ValueError("LLM answer is empty.")

    code, sanitization_time = models.sanitize_llm_answer(answer)
    logging.info(f"Code extraction time: {sanitization_time}")
    logging.info("Code extracted:")
    print(code)

    if not code:
        logging.error("LLM returned no Python code!")
        raise ValueError("LLM answer has no Python code.")

    logging.info(
        f"Saving code to {heuristic_file}."
    )

    experiment = ExperimentConfig(
        model_name=model,
        domain=domain,
        temperature=temperature,
        top_p=top_p,
        instance1=instance1,
        instance2=instance2,
        generated_heuristic=code,
        heuristic_generation_runtime=model_response_time
    )

    experiment_log = os.makedirs(f"{log_path}/{model}-{domain}-{temperature}-{top_p}", exist_ok=True)

    with open(f"{experiment_log}/logs.json", "w") as f:
        json.dump(asdict(experiment), f, indent=4)
        
    with open(heuristic_file, "w") as f:
        f.write(code)
        f.close()

    logging.info("Finished correctly.")


if __name__ == "__main__":
    _, total_runtime = main()
    logging.info(f"Total heuristic generation runtime: {total_runtime}") 