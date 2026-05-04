# from dateutil.parser import parse # how did these get here?
# from pkg_resources import require
import os
import csv
import subprocess
import json
import argparse
from time import perf_counter
from dataclasses import dataclass, asdict

from src.utils import PlanValidationConfig, timer
from src.llm_heuristics.suites import SUITES

parser: argparse.ArgumentParser = argparse.ArgumentParser()

parser.add_argument(
    "--base_path",
    type=str,
    help="base path to the external dataset"
)

parser.add_argument(
    "--domain",
    type=str,
    required=True,
    help="Name of Domain"
)

parser.add_argument(
    "--log_path",
    required=True,
    help="Directory to read and write logs to"
)

parser.add_argument(
    "--heuristic_file",
    required=True,
    help="File where learnt heuristic is stored"
)

parser.add_argument(
    "--problem_dir",
    required=True,
    type=str,
    help="Directory of problem files to evaluate"
)

parser.add_argument(
    "--timeout",
    rewuired=True,
    help="Timeout value"
)

parser.add_argument(
    "--experiment_name", # DeepSeepk-R1-blocksworld-temp_1_0-top_p-0_5
    required=True,
    help="path to heuristic logfile. Necessary to retrieve the experiment configuration"
)

args=parser.parse_args()

@timer
def run_pyperplan(domain, problem_file, timeout):
    cmd = [
       "uv run src/pyperplan/pyperplan.py",
        "-s", "gbfs_early_goal_test",
        "-H", f"{args.heuristic_file}",
        f"{domain}",
        f"{problem_file}" 
    ]

    result = subprocess.run(
        cmd, 
        timeout=timeout,
        stdout=subprocess.PIPE
    )

    # sanitize command output and get status
    data = json.loads(
        result.stdout.splitlines()[-1]
    )
    status = data["status"]
    return status


def main(args):
    domain_data_dir = f"{args.base_path}/{args.domain}"
    domain_file = f"{domain_data_dir}/domain.pddl"
    problem_files = f"{domain_data_dir}/{args.problem_dir}"
    experiment_dir = f"{args.log_path}/{args.experiment_name}"
    validate_file = os.path.exists(f"{experiment_dir}/validate.csv")

    with open(f"{experiment_dir}/logs.json") as f:
        heuristic_gen_config = json.load(f)

    for p_file in problem_files:
        problem_file = f"{domain_data_dir}/{p_file}"
        status, val_runtime = run_pyperplan(domain_file, problem_file, args.timeout)
        
        exp = PlanValidationConfig(
            temperature=heuristic_gen_config['temperature'],
            top_p=heuristic_gen_config['top_p'],
            evaluation_instance=p_file,
            prompt_instance1=heuristic_gen_config['instance1'],
            prompt_instance2=heuristic_gen_config['instance2'],
            generated_heuristic=heuristic_gen_config['generated_heuristic'],
            val_runtime=val_runtime,
            status=status
        )

        with open(validate_file, "a", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=asdict(exp).keys()
            )
            if not validate_file:
                writer.writeheader()
            writer.writerow(asdict(exp))
        



if __name__=="__main__":
    main(args)
