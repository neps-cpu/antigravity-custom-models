import sys
import urllib.request
import json

def query_openrouter(prompt: str, model: str = "anthropic/claude-3.5-sonnet"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer sk-or-v1-YOUR_OPENROUTER_API_KEY", # Replace with actual OpenRouter key
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Antigravity IDE"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            choices = res.get("choices", [])
            if choices:
                print(choices[0]["message"]["content"])
            else:
                print(json.dumps(res, indent=2))
    except Exception as e:
        print(f"Error querying OpenRouter: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python query.py <prompt> [model]")
        sys.exit(1)
    prompt = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "anthropic/claude-3.5-sonnet"
    query_openrouter(prompt, model)
