import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENROUTER_API_KEY')
if not api_key:
    print("No API key found")
    exit(1)

try:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    response.raise_for_status()
    data = response.json()
    print("API key is valid. Response:", data["choices"][0]["message"]["content"])
except Exception as e:
    print(f"API key invalid or error: {e}")