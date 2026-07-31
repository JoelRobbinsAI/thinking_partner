from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Conversation:
    id: str
    title: str
    workspace: str
    model: str
    created: datetime
    filepath: Path
    content: str

    @property
    def filename(self):
        return self.filepath.name

    def save(self):
        self.filepath.write_text(self.content)

    def _append_message(self, role: str, text: str):
        self.content += f"\n\n## {role}\n\n{text}"
        self.save()

    def append_user(self, text: str):
        self._append_message("User", text)

    def append_assistant(self, text: str):
        self._append_message("Assistant", text)

    def to_messages(self, system_prompt=None):
        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        lines = self.content.splitlines()

        role = None
        buffer = []

        for line in lines:
            if line.startswith("## User"):
                if role and buffer:
                    messages.append(
                        {
                            "role": role,
                            "content": "\n".join(buffer).strip(),
                        }
                    )
                role = "user"
                buffer = []

            elif line.startswith("## Assistant"):
                if role and buffer:
                    messages.append(
                        {
                            "role": role,
                            "content": "\n".join(buffer).strip(),
                        }
                    )
                role = "assistant"
                buffer = []

            elif role:
                buffer.append(line)

        if role and buffer:
            messages.append(
                {
                    "role": role,
                    "content": "\n".join(buffer).strip(),
                }
            )

        return messages