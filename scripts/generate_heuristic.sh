#!/bin/bash
source .venv/bin/activate

export CUDA_VISIBLE_DEVICES=0
echo "Using CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

#serve LLM model using vllm in a background process
MODEL_NAME="/scratch/common_models/Llama-3.2-3B-Instruct"
bash init_inference_server.sh "$MODEL_NAME" &

until curl -s http://localhost:8000/v1/models | grep -q "id"; do
  echo "Waiting for model to load..."
  sleep 2
done

echo "Model is loaded"

python llm-heuristics.py \
    --base_path benchmarks/ipc2023-learning/training/blocksworld \
    --domain "blocksworld" \
    --problem_dir instance_files \
    --instance1 p01.pddl \
    --instance2 p10.pddl \
    --framework "local" \
    --model "$MODEL_NAME" \
    --heuristic-file "heuristics/llama-3.2-3B_heuristic.py" \