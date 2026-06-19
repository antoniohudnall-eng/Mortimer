# Model Router Integration v3.1

## Quick Start
Import the integration in your agent controller:

```python
from model_router_integration import decide, speak, reason, code, ask, analyze

# Decision making
action, confidence = decide({"novelty": 0.8, "phase": "Explore"})

# Voice/Chat
response = speak("Hello", {"situation": "greeting"})

# Complex reasoning
analysis = reason("Explain quantum computing")

# Code generation
code_result = code("Sort a list", "python")

# General questions
answer = ask("What is the capital of France?")

# Text analysis
summary = analyze("Long text...", "summarize")
```

## Available Models (8 total)
- **Bonsai-8b-q1_0** - 1-bit decisions (cached)
- **tinyllama** - Fast decision fallback
- **Mort_II** - Voice/natural language
- **nomic-embed-text** - Embeddings
- **qwen2.5:14b** - Complex reasoning
- **phi3:medium** - Code generation
- **llama3.1:latest** - General questions
- **mistral:latest** - Analysis (MoE)

## Bridge Endpoint
http://127.0.0.1:11435
