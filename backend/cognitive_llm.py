import time

from backend.llm import OpenRouterLLM


class CognitiveLLM:
    def __init__(self):
        self.model = "mistralai/mistral-nemo"
        self.llm = OpenRouterLLM(self.model)

    def generate(self, prompt):
        print(f"Thinking with {self.model}...")

        print("\n================ PROMPT ================\n")
        print(prompt)
        print("\n============== END PROMPT ==============\n")

        start = time.perf_counter()

        reflection = self.llm.generate(
            [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        end = time.perf_counter()

        duration = end - start

        print(f"Completed in {duration:.2f} seconds.")
        print(reflection)

        return (
            f"Model: {self.model}\n"
            f"Duration: {duration:.2f} seconds\n\n"
            f"{reflection}"
        )