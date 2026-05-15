import subprocess



def serve_local_model(model, host, port) -> None:
    cmd = [
        "vllm", "serve", model,
        "--host", host,
        "--port", port,
    ]
    subprocess.Popen(cmd)



