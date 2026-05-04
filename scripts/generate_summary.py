import csv
import json
import argparse
from dataclasses import asdict
from src.utils import DirectoryEvaluationConfig

parser = argparse.ArgumentParser()

parser.add_argument(
    "--log_dir"
    type=str,
    help="Path to base log directory"
)

parser.add_argument(
    "--experiment_name",
    type=str,
    help="Name of experiment to summarize"
)

args = parser.parse_args()

status_summary = {
    "success": [],
    "failure": [],
    "timeout": [],
    "no_solution": []
}

def main(args):
    experiment_dir = f"{args.log_dir}/{args.experiment_name}"
    csv_file = f"{experiment_dir}/validate.csv"
    heuristic_gen_config_file = f"{experiment_dir}/logs.json"
    summary_file = f"{experiment_dir}/summary.json"
    with open(heuristic_gen_config_file) as f:
        heuristic_gen_config = json.load(f)
    
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            status = row['status']
            status_summary[status].append(row['evaluation_instance'])

    
    summary = DirectoryEvaluationConfig(
        model=heuristic_gen_config['model'],
        domain=heuristic_gen_config['domain'],
        prompt_instance1=heuristic_gen_config['instance1'],
        prompt_instance2=heuristic_gen_config['instance2'],
        temperature=heuristic_gen_config['temperature'],
        top_p=heuristic_gen_config['top_p'],
        success=status_summary['success'],
        failure=status_summary['failure'],
        timeout=status_summary['timeout'],
        no_solution=status_summary['no_solution']
    )

    with open(summary_file, "w") as f:
        json.dump(asdict(summary), f)
    


