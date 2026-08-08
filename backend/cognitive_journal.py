from datetime import datetime
from pathlib import Path


class CognitiveJournal:
    def __init__(self, filename):
        self.filepath = Path("cognitive_journals") / filename

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

    def read_recent(self, count=2):
        if not self.filepath.exists():
            return ""

        content = self.filepath.read_text(
            encoding="utf-8"
        )

        entries = content.split("\n# ")

        if len(entries) <= 1:
            return content.strip()

        recent = entries[-count:]

        return "\n\n# ".join(
            entry.strip()
            for entry in recent
        )