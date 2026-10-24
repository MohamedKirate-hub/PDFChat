from rag_system.augemntation import Augment
from dotenv import load_dotenv
import requests
import os

load_dotenv()

class Generation:
    def __init__(self, model_name: str, history=None):
        api_key = os.getenv("API_KEY")
        self.history = history or []
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.header = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.payload = {
            "model": "nvidia/nemotron-3.5-super-vl:free",
            "messages": [],
        }

    def set_documents(self, documents):
        self.documents = documents
        self.augment = Augment(self.documents, self.history)

    def generate(self, query):
        prompt_template = self.augment.build_prompt(query)    
        self.payload["messages"] = prompt_template

        response = requests.post(
            self.url,
            headers=self.header,
            json=self.payload
        )
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        return answer