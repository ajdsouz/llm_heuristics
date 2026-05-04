import os
import shutil
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--base_path", type=str, help="Path to directory containing the data")
parser.add_argument("--domain", type=str, help="Name of domain to process")
# parser.add_argument("")
args = parser.parse_args()
domain_path = f"{args.base_path}/{args.domain}"
instances_directory = f"{domain_path}/instance_files"

os.makedirs(instances_directory, exist_ok=True)
original_contents = os.listdir(domain_path)
for c in original_contents:
    if c not in ["domain.pddl", "example-state.out", "example-static.out", "instance_files"]:
        # print(c)
        # num=int(c[1:-5])
        shutil.copy(f"{domain_path}/{c}", f"{instances_directory}/{c}")