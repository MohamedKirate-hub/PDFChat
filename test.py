
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY is missing from .env")

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

payload = {
    "model": "nvidia/nemotron-3.5-super-vl:free",
    "messages": [
        {
            "role": "user",
            "content": "Explain what a RAG system is in 3 simple sentences."
        }
    ],
}

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    print("API connection successful!")
    print("\nModel response:")
    print(answer)

except requests.exceptions.RequestException as exc:
    print("API request failed:", exc)
    if exc.response is not None:
        print("Details:", exc.response.text)
