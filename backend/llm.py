import os

from dotenv import load_dotenv
import requests


load_dotenv()


class OpenRouterLLM:
    def __init__(self, model: str):
        self.model = model

        self.api_key = os.environ["OPENROUTER_API_KEY"]

        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, messages):
        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        print("\n========== OPENROUTER RESPONSE ==========")
        print(data)
        print("======== END OPENROUTER RESPONSE ========\n")

        return data["choices"][0]["message"]["content"]