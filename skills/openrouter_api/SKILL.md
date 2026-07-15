---
name: openrouter-api
description: Query the OpenRouter API (e.g., Claude 3.5 Sonnet, GPT-4o) for answers to general or programming questions. Use when external AI model assistance is needed.
---

# OpenRouter API Skill

This skill teaches the agent how to communicate with the OpenRouter API endpoint.

## How to use

Run the python query script:
```bash
python scripts/query.py "your question here" [optional_model_name]
```

## Configuration

* **Endpoint:** `https://openrouter.ai/api/v1/chat/completions`
* **Authorization:** `Bearer sk-or-v1-YOUR_OPENROUTER_API_KEY`
* **Default Model:** `anthropic/claude-3.5-sonnet`
