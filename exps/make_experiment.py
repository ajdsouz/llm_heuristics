import json
import logging
import argparse
from template import template

def generate_experiment(template, args):
    return template.format(**args)


if __name__=="__main__":

    parser = argparse.ArgumentParser()

    # parser.add_argument(
    #     "--benchmarks_dir",
    #     type=str,
    #     help="Path to directory of benchmarks"
    # )

    # parser.add_argument(
    #     "--domain",
    #     type=str,
    #     help="Domain name"
    # )

    parser.add_argument(
        "--experiment_dir",
        type=str,
        help="Directory of experiment logs"
    )

    parser.add_argument(
        "--benchmarks_dir",
        type=str,
        help="Directory of benchmarks"
    )

    parser.add_argument(
        "--version",
        type=str,
        choices=["orig", "ipcv1", "ipcv2", "ipcv3"],
        default="orig"
        help="Version of benchmark to choose"
    )
    parser.add_argument(
        "--num_procs",
        type=int,
        help="Number of process to spawn"
    )

    parser.add_argument(
        "--time_limit",
        type=int,
        help="timelimit to run the heuristics"
    )

    parser.add_argument(
        "--memory_limit",
        type=int,
        help="Memory timit to run the heuristic"
    )

    parser.add_argument(
        "--split",
        choices=['training', 'testing'],
        default='training',
        help="Which split to run the experiment, training or testing"
    )

    parser.add_argument(
        "--subset",
        choices=['easy', 'medium', 'hard'],
        default='easy',
        help="What subset top work with; choices are easy, medium and hard."
    )

    # parser.add_argument(
    #     "--model_name",
    #     type=str,
    #     help="Name of model used to generate heuristic; used as algorithm in template"
    # )

    parser.add_argument

    args=parser.parse_args()

    with open(f"{args.experiment_dir}/logs.jsonl", "r") as jlf:
        entry = json.loads(next(jlf))

    exp_data = {
        'domain': entry['domain'],
        'model_name': entry['model_name']
    }

    data_dict = vars(args)
    data_dict.update(exp_data)

    exp_script = f"exps/{exp_data['model_name']}-{exp_data['domain']}-{args.version}.py"

    code = generate_experiment(template, data_dict)

    with open(exp_script, "w") as f:
        f.write(code)

    logging.info(f"Saved experiment script to {exp_script}")

    

    



