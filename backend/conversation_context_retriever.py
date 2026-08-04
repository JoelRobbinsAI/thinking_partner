from pathlib import Path


class ConversationContextRetriever:
    def __init__(self, conversations_dir):
        self.conversations_dir = Path(conversations_dir)

    def retrieve(self):
        conversations = sorted(
            self.conversations_dir.glob("*.md"),
            reverse=True,
        )

        if not conversations:
            return ""

        content = conversations[0].read_text(
            encoding="utf-8"
        )

        lines = content.splitlines()

        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == "## User":
                return "\n".join(lines[i + 1:]).strip()

        return ""