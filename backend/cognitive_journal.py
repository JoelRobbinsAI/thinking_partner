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

    def _read_entries(self):
        if not self.filepath.exists():
            return []

        content = self.filepath.read_text(
            encoding="utf-8"
        )

        if not content.strip():
            return []

        entries = content.split("\n# ")

        return [
            entry.strip()
            for entry in entries
            if entry.strip()
        ]

    def read_recent(self, count=2):
        entries = self._read_entries()

        if not entries:
            return ""

        recent = entries[-count:]

        return "\n\n# ".join(recent)

    def _unconsolidated_entries(self):
        entries = self._read_entries()

        last_consolidation = -1

        for index, entry in enumerate(entries):
            if "Job: Consolidation" in entry:
                last_consolidation = index

        return entries[last_consolidation + 1:]

    def read_for_consolidation(self, count=4):
        entries = self._unconsolidated_entries()

        if len(entries) < count:
            return ""

        batch = entries[:count]

        return "\n\n# ".join(batch)

    def replace_recent(
        self,
        job,
        reflection,
        count=4,
    ):
        entries = self._read_entries()

        if not entries:
            return

        last_consolidation = -1

        for index, entry in enumerate(entries):
            if "Job: Consolidation" in entry:
                last_consolidation = index

        start = last_consolidation + 1
        end = start + count

        if len(entries) < end:
            return

        remaining = (
            entries[:start]
            + entries[end:]
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        consolidated_entry = (
            f"{timestamp}\n\n"
            f"Job: {job}\n\n"
            f"{reflection}"
        )

        remaining.insert(
            start,
            consolidated_entry,
        )

        new_content = "\n# ".join(
            remaining
        )

        self.filepath.write_text(
            "# " + new_content + "\n",
            encoding="utf-8",
        )