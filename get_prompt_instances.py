import os
import json
import argparse
from tarski.io import PDDLReader

def count_objects(problem) -> int:
    return len(problem.language.constants())

def find_instances(domain, instance_directory) -> tuple[str, str]:
    """
    Finds instance files with smallest and largest number of
    objects

    Args:
        domain (str): Path to domain file
        instance_directory (_type_): path to instance directory
    """
    results = []

    for file in os.listdir(instance_directory):
        print(f"processing instance {file}")
        if not file.endswith(".pddl"):
            continue
        instance = os.path.join(instance_directory, file)
        # reader.parse_domain(domain)
        reader = PDDLReader(raise_on_error=True)
        reader.parse_domain(domain)
        problem=reader.parse_instance(instance)
        n_objects = count_objects(problem)
        results.append((file, n_objects))

    if not results:
        print("No pddl files found!")
        return
    
    smallest = min(results, key=lambda x: x[1])
    largest = max(results, key=lambda x: x[1])
    # TODO maintain parity in instances chosen (use numbers /) 
    # return smallest, largest
    print(f"Smallest problem instance is : {smallest}")
    print(f"Largest problem instance is : {largest}")

    return smallest, largest

    

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--domain_dir", help="Path to domain directory")
    parser.add_argument("--instance_dir", help="Path to instance directory")
    # parser.add_argument("--experiment_dir", type=str, help="Path to experiment directory")
    args=parser.parse_args()
    domain_file = f"{args.domain_dir}/domain.pddl"
    smallest, largest = find_instances(domain_file, args.instance_dir)

    instance_dict = {
        "smallest": smallest,
        "largest": largest
    }

    with open(f'{args.domain_dir}/prompt_instances.json', "w") as f:
        json.dump(instance_dict, f, indent=4)

    