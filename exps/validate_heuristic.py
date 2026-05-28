#! /usr/bin/env python

import glob
import os
import sys
import json
import argparse

from random import shuffle

from downward.reports.absolute import AbsoluteReport

from lab.environments import BaselSlurmEnvironment, LocalEnvironment
from lab.experiment import Experiment
from lab.reports import Attribute

from parser import make_parser

from project import *

from src.utils import HeuristicGenerationConfig

parser = argparse.ArgumentParser()

parser.add_argument(
    "--experiment_dir",
    type=str,
    help="Path to the experiment base directory"
)

parser.add_argument(
    "--experiment_name",
    type=str,
    help="Name of (folder) experiment"
)

parser.add_argument(
    "--benchmarks",
    type=str,
    help="Path to the directory containing the benchmarks"
)

parser.add_argument(
    "--split",
    type=str,
    choices=['training', 'testing'],
    default='training'
    help="Split of data to experiment with. Possible values are `'training'` and `'testing'`. Defaults to `training`"
)

parser.add_argument(
    "--subset",
    type=str,
    choices=['easy', 'medium', 'hard'],
    default='easy'
    help="Subset of data to experiment with. Possible values are `'easy'`, `'medium'` and `'hard'`. Defaults to `'easy'`"
)


args = parser.parse_args()
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

#REMOTE = is_remote()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
#BENCHMARKS_DIR = os.path.join(SCRIPT_DIR, "../benchmarks/ipc2023-learning/training")
BENCHMARKS_DIR = args.benchmarks
#HEURISTICS = ['_'.join([str(i+1), j]) for i in range(25) for j in ['10']]

#DOMAINS = IPC2023_DOMAINS
TIME_LIMIT = 300
MEMORY_LIMIT = 8192
experiment_path = f"{args.experiment_dir}/{args.experiment_name}"
with open(f"{experiment_path}/logs.json", "r") as exp_log:
    heuristic_gen_log = json.load(exp_log)

HEURISTICS = os.listdir(os.path.join(experiment_path, "heuristics"))
#heuristic_gen_log = HeuristicGenerationConfig(**data)

ENV = LocalEnvironment(processes=4)
    # Use smaller suite for local tests.
SUITE = make_suite(heuristic_gen_log['domain'], BENCHMARKS_DIR, split=args.split, subset=args.subset) #should work, giving 

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
exp = Experiment(environment=ENV, path=experiment_path)
# Add solver to experiment and make it available to all runs.
#exp.add_resource("solver", os.path.join(SCRIPT_DIR, "solver.py"))
# Add custom parser.
exp.add_parser(make_parser())

for domain, task in SUITE:
    for h_file in HEURISTICS:
        #algorithm = ''.join(['gemini', h])
        algorithm = heuristic_gen_log['model_name']
        heur = os.path.join(experiment_path, "heuristics", h_file)
        run = exp.add_run()
        # Create a symbolic link and an alias. This is optional. We
        # could also use absolute paths in add_command().
        run.add_resource("task", task, symlink=True)
        run.add_command(
            "plan",
            [sys.executable, os.path.join(SCRIPT_DIR, "../src/pyperplan/pyperplan.py"), "-H", heur, "-s", "gbf", task],
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
