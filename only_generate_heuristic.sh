#!/bin/bash
source .venv/bin/activate

MODEL_NAME=$1

python generate_heuristic.py \
    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
    --log_path /scratch/a7_data/llm_heuristics \
    --domain blocksworld \
    --problem_dir training/easy \
    --framework "local" \
    --model "$MODEL_NAME" \
    --n_prompts 25 \
    --temperature 0.6 \
    --top-p 0.95


python generate_heuristic.py \
    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
    --log_path /scratch/a7_data/llm_heuristics \
    --domain ferry \
    --problem_dir training/easy \
    --framework "local" \
    --model "$MODEL_NAME" \
    --n_prompts 25 \
    --temperature 0.6 \
    --top-p 0.95

python generate_heuristic.py \
    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
    --log_path /scratch/a7_data/llm_heuristics \
    --domain goldminer \
    --problem_dir training/easy \
    --framework "local" \
    --model "$MODEL_NAME" \
    --n_prompts 25 \
    --temperature 0.6 \
    --top-p 0.95


# python generate_heuristic.py \
#    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
#    --log_path /scratch/ajdsouza/llm_heuristics/tests/log \
#    --domain grippers \
#    --problem_dir training/easy \
#    --framework "local" \
#    --model "$MODEL_NAME" \
#    --n_prompts 25


python generate_heuristic.py \
    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
    --log_path /scratch/a7_data/llm_heuristics \
    --domain rovers \
    --problem_dir training/easy \
    --framework "local" \
    --model "$MODEL_NAME" \
    --n_prompts 25 \
    --temperature 0.6 \
    --top-p 0.95


python generate_heuristic.py \
    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
    --log_path /scratch/a7_data/llm_heuristics \
    --domain visitall \
    --problem_dir training/easy \
    --framework "local" \
    --model "$MODEL_NAME" \
    --n_prompts 25 \
    --temperature 0.6 \
    --top-p 0.95


python generate_heuristic.py \
    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
    --log_path /scratch/a7_data/llm_heuristics \
    --domain depot \
    --problem_dir training/easy \
    --framework "local" \
    --model "$MODEL_NAME" \
    --n_prompts 25 \
    --temperature 0.6 \
    --top-p 0.95


python generate_heuristic.py \
    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
    --log_path /scratch/a7_data/llm_heuristics \
    --domain floortile \
    --problem_dir training/easy \
    --framework "local" \
    --model "$MODEL_NAME" \
    --n_prompts 25 \
    --temperature 0.6 \
    --top-p 0.95


python generate_heuristic.py \
    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
    --log_path /scratch/a7_data/llm_heuristics \
    --domain grid \
    --problem_dir training/easy \
    --framework "local" \
    --model "$MODEL_NAME" \
    --n_prompts 25 \
    --temperature 0.6 \
    --top-p 0.95


# python generate_heuristic.py \
#    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
#    --log_path /scratch/ajdsouza/llm_heuristics/tests/log \
#    --domain logistics \
#    --problem_dir training/easy \
#    --framework "local" \
#    --model "$MODEL_NAME" \
#    --n_prompts 25


python generate_heuristic.py \
    --base_path /scratch/ajdsouza/katharina-data/data_for_anthony/data_costumed/data_costumed_ipc_v1/ \
    --log_path /scratch/a7_data/llm_heuristics \
    --domain satellite \
    --problem_dir training/easy \
    --framework "local" \
    --model "$MODEL_NAME" \
    --n_prompts 25 \
    --temperature 0.6 \
    --top-p 0.95
