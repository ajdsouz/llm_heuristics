#!/bin/bash

MODEL_PATH=$1
HOST = "127.0.0.1"
PORT = "8000"

vllm serve "$MODEL_PATH" \
    --host "$HOST" \
    --port "$PORT"