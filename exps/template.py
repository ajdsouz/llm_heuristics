template = '''
import glob
import os
import sys

from random import shuffle

from downward.reports.absolute import AbsoluteReport

from lab.environments import BaselSlurmEnvironment, LocalEnvironment
from lab.experiment import Experiment
from lab.reports import Attribute

from parser import make_parser

from project import *

# Create custom report class with suitable info and error attributes.
class BaseReport(AbsoluteReport):
    INFO_ATTRIBUTES = ["time_limit", "memory_limit"]
    ERROR_ATTRIBUTES = [
        "domain",
        "problem",
        "algorithm",
        "unexplained_errors",
        "error",
        "node",
    ]

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEURISTICS_DIR = '{experiment_dir}heuristics'
HEURISTICS = [f for f in os.listdir(HEURISTICS_DIR) if f.endswith('.py')]
BENCHMARKS_DIR = '{benchmarks_dir}'
DOMAIN = '{domain}'
TIME_LIMIT = {time_limit}
MEMORY_LIMIT = {memory_limit}


ENV = LocalEnvironment(processes={num_procs})
SUITE = make_suite(DOMAIN, BENCHMARKS_DIR, split='{split}', subset='{subset}')

ATTRIBUTES = [
    "plan_length",
    "search_time",
    "expansions",
    "error",
    "initial_h_value",
    'score_agile',
    'score_expansion',
    "coverage",
]



# Create a new experiment.
exp = Experiment(environment=ENV, path='{experiment_dir}exps/{split}/{subset}')
# Add solver to experiment and make it available to all runs.
#exp.add_resource("solver", os.path.join(SCRIPT_DIR, "solver.py"))
# Add custom parser.
exp.add_parser(make_parser())

for domain, domain_file, task in SUITE:
    for h in HEURISTICS:
    
        algorithm = '-'.join(['{model_name}', h])
    
        heur = os.path.join(HEURISTICS_DIR, h)

        run = exp.add_run()
        # Create a symbolic link and an alias. This is optional. We
        # could also use absolute paths in add_command().
        run.add_resource("task", task, symlink=True)
        run.add_resource("domain", domain_file, symlink=True) 
        run.add_command(
            "plan",
            [sys.executable, os.path.join(PROJECT_DIR, "src/pyperplan/pyperplan.py"), "-H", heur, "-s", "gbf", domain_file, task],
            time_limit=TIME_LIMIT,
            memory_limit=MEMORY_LIMIT,
        )

        task_name = os.path.basename(task)
        run.set_property("domain", domain)
        run.set_property("problem", task_name)
        run.set_property("algorithm", algorithm)
        # BaseReport needs the following properties:
        # 'time_limit', 'memory_limit', 'seed'.
        run.set_property("time_limit", TIME_LIMIT)
        run.set_property("memory_limit", MEMORY_LIMIT)
        # Every run has to have a unique id in the form of a list.
        run.set_property("id", [algorithm, domain, task_name])


# Add step that writes experiment files to disk.
exp.add_step("build", exp.build)

# Add step that executes all runs.
exp.add_step("start", exp.start_runs)

# Add step that parses the logs.
exp.add_step("parse", exp.parse)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name="fetch")

# Make a report.
add_absolute_report(exp, attributes=ATTRIBUTES,
                    filter=[get_agile_score, get_expansion_score])


# Parse the commandline and run the given steps.
exp.run_steps()
'''
