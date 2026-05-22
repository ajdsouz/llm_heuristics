#!bin/bash

python validate_heyristic.py \
    --base_path /nethome/ajdsouza/llm_heuristics/benchmarks/ipc2023-learning/training \
    --domain blocksworld \
    --log_path /scratch/ajdsouza/llm_heuristics/logs/tests/ \
    --heuristic_file /path/to/heuristics/file \
    --problem_dir instance_files \
    --timeout 1800 \
    --experiment_name {experiment_name}