#llm.py

import os
import time
from dotenv import load_dotenv
import requests


load_dotenv()


class OpenRouterLLM:
    def __init__(self, model: str):
        self.model = model
        self.api_key = os.environ["OPENROUTER_API_KEY"]
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def generate(self, messages):
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "timeout": 60,  # Add timeout parameter
                    },
                    timeout=120,
                )

                response.raise_for_status()
                data = response.json()

                print("\n========== OPENROUTER RESPONSE ==========")
                print(data)
                print("======== END OPENROUTER RESPONSE ========\n")

                # Check for error response
                if "error" in data:
                    error_msg = data["error"].get("message", "Unknown error")
                    print(f"❌ OpenRouter error: {error_msg}")
                    
                    if attempt < self.max_retries - 1:
                        print(f"  Retrying in {self.retry_delay} seconds... (Attempt {attempt + 2}/{self.max_retries})")
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        return f"I apologize, but I encountered an error: {error_msg}. Please try again."

                # Check if choices exist
                if "choices" not in data or not data["choices"]:
                    print("❌ No choices in response")
                    if attempt < self.max_retries - 1:
                        print(f"  Retrying in {self.retry_delay} seconds... (Attempt {attempt + 2}/{self.max_retries})")
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        return "I apologize, but I received an empty response. Please try again."

                return data["choices"][0]["message"]["content"]

            except requests.exceptions.Timeout:
                print(f"❌ Request timed out (Attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    print(f"  Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return "I apologize, but the request timed out. Please try again."

            except requests.exceptions.RequestException as e:
                print(f"❌ Request error: {e}")
                if attempt < self.max_retries - 1:
                    print(f"  Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return f"I apologize, but I encountered a connection error: {e}. Please try again."

            except KeyError as e:
                print(f"❌ Unexpected response format: {e}")
                if attempt < self.max_retries - 1:
                    print(f"  Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return "I apologize, but I received an unexpected response. Please try again."

        return "I apologize, but I'm having trouble responding right now. Please try again."