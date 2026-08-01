from datetime import datetime
from pathlib import Path


class ReflectionManager:
    def __init__(self, workspace):
        self.reflections_dir = (
            Path(workspace.workspace) / "reflections"
        )

        self.reflections_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save_reflection(
        self,
        conversation,
        reflection,
    ):
        filename = (
            conversation.filepath.stem + "_reflection.md"
        )

        filepath = (
            self.reflections_dir / filename
        )

        content = (
            f"# Reflection\n\n"
            f"Conversation: {conversation.filename}\n"
            f"Created: {datetime.now().isoformat()}\n\n"
            f"{reflection}\n"
        )

        filepath.write_text(content)

        return filepath