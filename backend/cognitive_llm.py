import time
import os
from backend.llm import OpenRouterLLM


class CognitiveLLM:
    def __init__(self, model=None):
        # Use the same model as the conversation interface, or fallback
        if model is None:
            # Try to get from environment or use default
            self.model = os.environ.get("COGNITIVE_MODEL", "openai/gpt-oss-120b")
        else:
            self.model = model
        self.llm = OpenRouterLLM(self.model)

    def generate(self, prompt):
        print(f"Thinking with {self.model}...")

        print("\n================ PROMPT ================\n")
        print(prompt)
        print("\n============== END PROMPT ==============\n")

        start = time.perf_counter()

        # Retry logic
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                reflection = self.llm.generate(
                    [
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ]
                )
                
                # Check if we got an error message
                if reflection and "error" in reflection.lower():
                    if attempt < max_retries - 1:
                        print(f"  ⚠️ Error received, retrying in {retry_delay}s... (Attempt {attempt + 2}/{max_retries})")
                        time.sleep(retry_delay)
                        continue
                
                end = time.perf_counter()
                duration = end - start
                print(f"Completed in {duration:.2f} seconds.")
                print(reflection)
                
                return (
                    f"Model: {self.model}\n"
                    f"Duration: {duration:.2f} seconds\n\n"
                    f"{reflection}"
                )
                
            except Exception as e:
                print(f"  ⚠️ Error: {e}")
                if attempt < max_retries - 1:
                    print(f"  Retrying in {retry_delay}s... (Attempt {attempt + 2}/{max_retries})")
                    time.sleep(retry_delay)
                    continue
                else:
                    # Return a fallback reflection
                    return (
                        f"Model: {self.model}\n"
                        f"Duration: 0.00 seconds\n\n"
                        f"Error encountered after {max_retries} attempts. Please check the logs and try again."
                    )