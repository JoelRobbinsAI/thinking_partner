from datetime import datetime
from pathlib import Path


class CognitiveLog:
    def __init__(self):
        self.filepath = Path("cognitive_log.md")

    def append(self, job, reflection):
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
                f"{reflection}\n\n"
            )

    def read(self):
        if not self.filepath.exists():
            return ""

        return self.filepath.read_text(
            encoding="utf-8"
        )