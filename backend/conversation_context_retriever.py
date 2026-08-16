from pathlib import Path
from typing import Optional


class ConversationContextRetriever:
    def __init__(
        self, 
        conversations_dir: str, 
        workspaces_root: Optional[str] = None,
        recent_messages_limit: int = 30
    ):
        """
        Initialize the conversation context retriever.
        
        Args:
            conversations_dir: Path to the conversations directory (relative to workspace)
            workspaces_root: Path to the workspaces root directory
            recent_messages_limit: Number of recent messages to include
        """
        self.conversations_dir = Path(conversations_dir)
        self.workspaces_root = Path(workspaces_root) if workspaces_root else None
        self.recent_messages_limit = recent_messages_limit
    
    def _get_active_workspace(self) -> Optional[Path]:
        """Find the most recently modified workspace."""
        if not self.workspaces_root:
            return None
        
        workspaces = sorted(
            [p for p in self.workspaces_root.iterdir() if p.is_dir()],
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        return workspaces[0] if workspaces else None
    
    def _get_system_prompt(self, workspace_path: Path) -> str:
        """Retrieve the system prompt from the workspace."""
        possible_paths = [
            workspace_path / "system_prompt.md",
            workspace_path / "system.md",
            workspace_path / "prompt.md",
        ]
        
        for path in possible_paths:
            if path.exists():
                content = path.read_text(encoding="utf-8")
                if content.strip():
                    return content.strip()
        
        return ""
    
    def retrieve(self) -> str:
        """Retrieve conversation context (system prompt + summaries + recent messages)."""
        parts = []
        
        # Find active workspace
        workspace_path = self._get_active_workspace()
        
        # 1. Get workspace system prompt
        if workspace_path:
            system_prompt = self._get_system_prompt(workspace_path)
            if system_prompt:
                parts.append(f"## System Prompt\n\n{system_prompt}")
        
        # 2. Determine conversations directory
        if workspace_path:
            conversations_dir = workspace_path / self.conversations_dir
        else:
            conversations_dir = self.conversations_dir
        
        # 3. Get the most recent conversation
        conversations = sorted(
            conversations_dir.glob("*.md"),
            reverse=True,
        )
        
        if not conversations:
            return "\n\n".join(parts) if parts else ""
        
        # Get the base name of the most recent conversation
        conversation_name = conversations[0].stem
        
        # 4. Get summaries (if they exist)
        summary_path = conversations_dir / f"{conversation_name}.summary.md"
        if summary_path.exists():
            summary_content = summary_path.read_text(encoding="utf-8")
            if summary_content.strip():
                parts.append(f"## Conversation Summaries\n\n{summary_content.strip()}")
        
        # 5. Get recent messages
        content = conversations[0].read_text(encoding="utf-8")
        recent_messages = self._get_recent_messages(content)
        if recent_messages:
            parts.append(f"## Recent Messages (last {self.recent_messages_limit} exchanges)\n\n{recent_messages}")
        
        return "\n\n".join(parts) if parts else ""
    
    def _get_recent_messages(self, content: str) -> str:
        """Extract the most recent messages from conversation content."""
        lines = content.splitlines()
        
        message_blocks = []
        current_block = []
        current_speaker = None
        
        for line in lines:
            if line.strip() == "## User":
                if current_block and current_speaker:
                    message_blocks.append((current_speaker, "\n".join(current_block).strip()))
                current_block = []
                current_speaker = "User"
            elif line.strip() == "## Assistant":
                if current_block and current_speaker:
                    message_blocks.append((current_speaker, "\n".join(current_block).strip()))
                current_block = []
                current_speaker = "Assistant"
            else:
                if current_speaker:
                    current_block.append(line)
        
        if current_block and current_speaker:
            message_blocks.append((current_speaker, "\n".join(current_block).strip()))
        
        recent_blocks = message_blocks[-self.recent_messages_limit:]
        
        formatted = []
        for speaker, message in recent_blocks:
            if message.strip():
                formatted.append(f"**{speaker}:**\n{message.strip()}")
        
        return "\n\n".join(formatted) if formatted else ""