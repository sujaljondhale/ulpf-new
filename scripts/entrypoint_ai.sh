#!/bin/sh
# Start Ollama server in background
ollama serve &
SERVER_PID=$!

echo "[ULPF-AI] Ollama server started with PID $SERVER_PID. Waiting for daemon to be ready..."
sleep 3

# Wait for Ollama to become responsive
for i in $(seq 1 30); do
  if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
    echo "[ULPF-AI] Ollama API online."
    break
  fi
  sleep 1
done

# Pre-pull default lightweight model in background if specified
MODEL_NAME="${OLLAMA_MODEL:-qwen2.5-coder:3b}"
echo "[ULPF-AI] Checking availability of SLM model: $MODEL_NAME"
ollama pull "$MODEL_NAME" &

# Wait for Ollama server process
wait $SERVER_PID
