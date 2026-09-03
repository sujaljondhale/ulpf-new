# Air-Gapped Offline Deployment Guide

ULPF is designed to operate 100% offline without Internet access or cloud APIs.

## 1. Preparation on Connected Machine
```bash
# 1. Download Docker images as tarballs
docker pull python:3.12-slim
docker pull ollama/ollama:latest
docker save -o python_312_slim.tar python:3.12-slim
docker save -o ollama_latest.tar ollama/ollama:latest

# 2. Download local SLM model weights
ollama pull qwen2.5-coder:3b
# Model files located in ~/.ollama/models

# 3. Download python package wheels
pip download -r requirements.txt -d wheels/
```

## 2. Transfer to Air-Gapped Network
Transfer `python_312_slim.tar`, `ollama_latest.tar`, model weights, `wheels/`, and ULPF repository via USB drive / optical disk to the air-gapped environment.

## 3. Offline Container Deployment
```bash
# Load Docker images offline
docker load -i python_312_slim.tar
docker load -i ollama_latest.tar

# Launch via Docker Compose
docker-compose up -d
```
