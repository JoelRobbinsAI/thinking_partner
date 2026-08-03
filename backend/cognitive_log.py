from datetime import datetime
from pathlib import Path


class CognitiveLog:
    def __init__(self):
        self.filepath = Path("cognitive_log.md")

    def append(self, job, question):
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with self.filepath.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                f"# {timestamp}\n\n"
                f"Job: {job}\n\n"
                f"Question:\n"
                f"{question}\n\n"
                f"## What happened?\n"
                f"Stub.\n\n"
                f"## What did I learn?\n"
                f"Stub.\n\n"
                f"## What should change?\n"
                f"Stub.\n\n"
            )