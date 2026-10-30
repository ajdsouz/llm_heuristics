#!/bin/bash

MODEL_PATH=$1
HOST="127.0.0.1"
PORT="8000"

# set variable so subsequent scripts can access model path / name
#export $MODEL_PATH

#export NCCL_P2P_DISABLE=1

vllm serve "$MODEL_PATH" \
    --enforce-eager \
    --host "$HOST" \
    --port "$PORT" \
    --tensor-parallel-size 2
    --reasoning-parser deepseek_r1
    # --reasoning-parser qwen3
    # --tensor-parallel-size 2
    # --max-model-lem 16384

