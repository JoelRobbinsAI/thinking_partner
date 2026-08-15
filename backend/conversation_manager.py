#Conversation Manager
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from .conversation import Conversation


class ConversationManager:
    def __init__(self, workspace):
        self.workspace = workspace
        self.conversations_dir = (
            Path(workspace.workspace) / "conversations"
        )
        self.conversations_dir.mkdir(parents=True, exist_ok=True)

    def create_conversation(self, title="New Conversation", model=None):
        conversation_id = str(uuid4())
        timestamp = datetime.now()

        filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.conversations_dir / filename

        # Use provided model, or fall back to workspace.model
        model_name = model if model else self.workspace.model

        content = f"""---
id: {conversation_id}
title: {title}
created: {timestamp.isoformat()}
workspace: {self.workspace.name}
model: {model_name}
---

# {title}
"""

        filepath.write_text(content)

        return filepath

    def list_conversations(self):
        """Return all conversation files, newest first."""
        return sorted(
            self.conversations_dir.glob("*.md"),
            reverse=True
        )

    def load_conversation(self, filepath):
        """Load a conversation and return a Conversation object."""

        content = filepath.read_text()

        lines = content.splitlines()

        metadata = {}

        if lines and lines[0] == "---":
            for line in lines[1:]:
                if line == "---":
                    break
                
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # Only process lines with a colon
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()

        return Conversation(
            id=metadata.get("id", ""),
            title=metadata.get("title", "Untitled"),
            workspace=metadata.get("workspace", ""),
            model=metadata.get("model", ""),
            created=datetime.fromisoformat(metadata.get("created", datetime.now().isoformat())),
            filepath=filepath,
            content=content,
        )
