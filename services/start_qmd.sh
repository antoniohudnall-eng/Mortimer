#!/bin/bash
cd ~/mortimer/services
source ~/.bashrc 2>/dev/null
export OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5:1.5b}"
export USE_OLLAMA="${USE_OLLAMA:-false}"
python3 qmd_service.py
