import time

import ollama


class CognitiveLLM:
    def __init__(self):
        self.model = "phi3:mini"

    def generate(self, prompt):
        print(f"Thinking with {self.model}...")

        start = time.perf_counter()

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            think=False,
        )

        end = time.perf_counter()

        duration = end - start

        print(f"Completed in {duration:.2f} seconds.")

        print(response)

        reflection = response["message"]["content"]

        return (
            f"Model: {self.model}\n"
            f"Duration: {duration:.2f} seconds\n\n"
            f"{reflection}"
        )