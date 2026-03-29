# !/bin/bash
source .venv/bin/activate

# serve LLM model using vllm
MODEL_NAME = "/scratch/common_models/Llama-3.2-1b"
bash init_inference_server.sh "$MODEL_NAME"

uv run llm-heuristics.py \
    --domain blocksworld \
    --framework local \
    --model /scratch.common_models/Llama-3.2-1b \
    --heuristic-file heuristics/blocksworld_heuristic.py \
    