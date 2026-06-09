#!/bin/bash
source .venv/bin/activate

export CUDA_VISIBLE_DEVICES=0
echo "Using CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

#serve LLM model using vllm in a background process
export MODEL_NAME="/scratch/common_models/Qwen3-30B-A3B-Thinking-2507"

echo "$MODEL_NAME"

bash init_inference_server.sh "$MODEL_NAME" &

until curl -s http://localhost:8000/v1/models | grep -q "id"; do
  echo "Waiting for model to load..."
  sleep 2
done

echo "Model is loaded"

echo "starting heuristic_generation"
bash only_generate_heuristic.sh /scratch/common_models/Qwen3-30B-A3B-Thinking-2507
# python generate_heuristic.py \
#     --base_path benchmarks/ipc2023-learning/training \
#     --log_path /scratch/ajdsouza/llm_heuristics/tests/log \
#     --domain blocksworld \
#     --problem_dir instance_files \
#     --framework "local" \
#     --model "$MODEL_NAME" 
