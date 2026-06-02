import dataclasses
import sys
import os
import json
from dataclasses import dataclass, asdict
import logging 
import argparse
from src.utils import timer, HeuristicGenerationConfig
from src.llm_heuristics import models
from src.llm_heuristics.suites import SUITES, DomainSuite
from src.llm_heuristics.prompt import create_prompt


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s :: %(message)s",
)
logger = logging.getLogger(__name__)


def validate_heuristic_name(value) -> str:
    if not value.endswith("Heuristic"):
        raise argparse.ArgumentTypeError("The heuristic name must end with 'Heuristic'.")
    return value


def validate_heuristic_file(value) -> str:
    if not value.endswith(".py"):
        raise argparse.ArgumentTypeError("The heuristic name must end with '.py'.")
    return value


def validate_temperature(value) -> float:
    if value > 2 or value < 0:
        raise argparse.ArgumentTypeError("The temperature must be in the interval [0,2].")
    return value

def validate_top_p(value) -> float:
    if value > 1 or value < 0:
        raise argparse.ArgumentTypeError("The top-P must be in the interval [0,1].")
    return value



    
@timer
def main(args, n_prompt):
    logging.info(f"Python version: {sys.version}.")
    logging.info(f"Using suite {args.domain}.")
    # suite = SUITES[domain]
    # if base_path is not None and domain not in SUITES:
    
    domain_data_folder: str = f"{args.base_path}/{args.domain}"
    with open(f"{domain_data_folder}/prompt_instances.json", "r") as jf:
        prompt_instances = json.load(jf)

    suite = DomainSuite(
        name=args.domain, 
        domain=f"{domain_data_folder}/domain.pddl",
        instance1=f"{domain_data_folder}/training/easy/{prompt_instances['smallest']}",
        instance2=f"{domain_data_folder}/training/easy/{prompt_instances['largest']}",
        state=f"{domain_data_folder}/example-state.out",
        static=f"{domain_data_folder}/example-static.out"
    )
    # elif base_path is None and domain not in SUITES:
    #     raise NotFoundErr("Domain not found in provided Suites and no base_path is provided."
    #     "Provide a valid base_path for unseen domains")
    # else:
    #     suite: DomainSuite = SUITES[domain]
    model_name = args.model
    if args.framework == "local":
        # extract model name from model path
        # /scratch/common_models/Llama-3.2-3B-Instruct -> Llama-3.2-3B-Instruct
        model_name = model_name.split("/")[-1]
        # Llama-3.2-3B-Instruct -> Llama-3_2-3B-Instruct
        model_name = model_name.replace(".", "_")
    else:
        model_name = model_name
    
    logging.info(f"Using model {model_name} with framework {args.framework}.")
    logging.info(f"Using temperature {args.temperature}.")
    logging.info(f"Using top-P {args.top_p}.")
    logging.info(f"Using ablation option {args.ablation}")
    logging.info(f"Generating prompt with format {args.prompt_format}")
    prompt, prompt_creation_time = create_prompt(suite, args.heuristic_name, args.prompt_format, args.ablation)
    logging.info(f"Time to generate prompt: {prompt_creation_time}")
    logging.info("Final prompt: ")
    print(prompt)

    #logging.info(f"Using model {args.model} with framework {args.framework}.")

    # if args.framework == "gemini":
    #     answer, input_token_count, output_token_count, model_response_time = models.run_gemini(args.model, args.prompt, args.temperature, args.top_p)
    if args.framework == "deepseek":
        (answer, input_token_count, output_token_count), model_response_time = models.run_deepseek(args.model, prompt, args.temperature, args.top_p)
    elif args.framework == "openai":
        (answer, input_token_count, output_token_count), model_response_time = models.run_openai(args.model, prompt, args.temperature, args.top_p)
    elif args.framework == "local":
        (answer, input_token_count, output_token_count), model_response_time = models.run_local(args.model, prompt, args.temperature, args.top_p)

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
    
    #TODO create heuristic file under experiment folder
    heuristic_file = f"{args.domain}_{n_prompt}.py"
    logging.info(
        f"Saving code to {heuristic_file}."
    )

    experiment = HeuristicGenerationConfig(
        model_name=model_name,
        domain=args.domain,
        temperature=args.temperature,
        top_p=args.top_p,
        instance1=f"{domain_data_folder}/training/easy/{prompt_instances['smallest']}",
        instance2=f"{domain_data_folder}/training/easy/{prompt_instances['largest']}",
        generated_heuristic=heuristic_file,
        model_response_time=model_response_time, 
        input_token_count=input_token_count,
        output_token_count=output_token_count
    )

    s_temperature = str(args.temperature).replace(".", "_")
    s_top_p = str(args.top_p).replace(".", "_")
    experiment_log = f"{args.log_path}/{model_name}-{args.domain}-temp-{s_temperature}-top_p-{s_top_p}"
    heuristics_dir = f"{experiment_log}/heuristics/"
    os.makedirs(heuristics_dir, exist_ok=True)
    with open(f"{heuristics_dir}/{heuristic_file}", "w") as f:
        f.write(code)
        f.close()
    
    logging.info("Finished correctly.")
    return experiment


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--base_path",
        type=str,
        help="Base path to the data directory",
    )

    parser.add_argument(
        "--log_path",
        help="Directory to write logs to",
    )

    parser.add_argument(
        "--domain",
        required=True,
        help="Name of the domain used. Everything else is inferred.",
    )
    parser.add_argument(
        "--problem_dir",
        required=True,
        help="The directory of problem instances. ",
    )

    # parser.add_argument(
    #     "--instance1",
    #     required=True,
    #     help="First problem file to use to build prompt. Preferable the smmallest problem instance.",
    # )

    # parser.add_argument(
    #     "--instance2",
    #     required=True,
    #     help="Second problem file to use to build prompt. Preferably the longest proble instance.",
    # )

    parser.add_argument(
        "--framework",
        choices=["deepseek", "openai", "local"],
        help="Framework used to run LLMs.",
    )

    parser.add_argument(
        "--model",
        default="gemini-2.0-flash-thinking",
        help="LLM Model used. If a local model is used, provide path to local model. The folder should have structure similar to a HF model repo",
    )
    parser.add_argument(
        "--heuristic-name",
        default="NewDomainDependentHeuristic",
        type=validate_heuristic_name,
        help="Name of the heuristic and of its class. Name must end with 'Heuristic'. \
        NOTE: This impacts how you will call it from pyperplan!",
    )
    # parser.add_argument(
    #     "--heuristic-file",
    #     default="new-heuristic.py",
    #     type=validate_heuristic_file,
    #     help="File where the learnt heuristic is stored. It must be a Python file.",
    # )
    parser.add_argument(
        "--prompt-format",
        default="neurips",
        choices=["base", "checklist", "goalcount", "new", "pyperplan", "reordered", "neurips"],
        help="Format of the prompt passed to the heuristic.",
    )

    parser.add_argument(
        "--temperature",
        default=1.0,
        type=validate_temperature,
        help="Model temperature.",
    )
    parser.add_argument(
        "--top-p",
        default=0.5,
        type=validate_top_p,
        help="Model top-P.",
    )

    parser.add_argument(
        "--n_prompts",
        type=int,
        help="Number of prompts"
    )

    parser.add_argument(
        "--ablation",
        default="false",
        choices=["false", "complete", "description_simple", "domain", "instances", "dependent-heuristics", "state-representation", "static-representation",
                        "planner-code", "checklist", "checklist-no6", "independent-heuristics", "heuristics-nocomment", "dependent-heuristics-and-plans"],
        help="Ablation options for reordered prompt.",
    )


    args = parser.parse_args()
    for n_prompt in range(args.n_prompts):
        experiment, total_runtime = main(args, n_prompt)
        experiment.heuristic_generation_runtime = total_runtime
        s_temperature = str(args.temperature).replace(".", "_")
        s_top_p = str(args.top_p).replace(".", "_")
        experiment_log = f"{args.log_path}/{experiment.model_name}-{args.domain}-temp-{s_temperature}-top_p-{s_top_p}"
        os.makedirs(experiment_log, exist_ok=True)

        with open(f"{experiment_log}/logs.jsonl", "a") as f:
            f.write(json.dumps(asdict(experiment)) + "\n")

    # logging.info(f"Total heuristic generation runtime: {total_runtime}") 
    # logging.info(f"Experiment saved at : {experiment_log}")