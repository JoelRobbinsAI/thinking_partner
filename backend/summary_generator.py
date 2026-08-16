import re
from pathlib import Path
from datetime import datetime
from backend.llm import OpenRouterLLM

class SummaryGenerator:
    def __init__(self, workspaces_dir: Path):
        self.workspaces_dir = workspaces_dir
        self.llm = OpenRouterLLM(model="mistralai/mistral-nemo:latest")
        self.chunk_size = 30  # messages per chunk
    
    def get_summary_file(self, workspace: str, conversation_id: str) -> Path:
        """Return path to the summary file for a conversation."""
        return self.workspaces_dir / workspace / f".{conversation_id}.summary.md"
    
    def get_existing_chunks(self, workspace: str, conversation_id: str) -> list:
        """Parse the summary file and return list of existing chunk numbers."""
        summary_file = self.get_summary_file(workspace, conversation_id)
        if not summary_file.exists():
            return []
        
        content = summary_file.read_text()
        # Find all ## Chunk N: timestamp → timestamp lines
        pattern = r"## Chunk (\d+):"
        matches = re.findall(pattern, content)
        return [int(m) for m in matches]
    
    def get_message_chunks(self, conversation) -> list:
        """Split conversation messages into chunks of chunk_size user+assistant pairs."""
        messages = conversation.to_messages()
        # Remove system prompt if present
        if messages and messages[0]["role"] == "system":
            messages = messages[1:]
        
        chunks = []
        for i in range(0, len(messages), self.chunk_size * 2):
            chunk = messages[i:i + self.chunk_size * 2]
            if chunk:
                chunks.append(chunk)
        return chunks
    
    def generate_summary(self, chunk_messages: list, chunk_num: int) -> str:
        """Generate a summary for a chunk of messages."""
        # Format messages for the summary prompt
        conversation_text = ""
        for msg in chunk_messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            conversation_text += f"\n**{role}:** {content}\n"
        
        prompt = f"""Summarize the following conversation segment. Focus on:
- Key topics discussed
- Decisions made
- Questions raised
- Changes in direction or understanding

Keep the summary concise but informative (3-5 paragraphs).

Conversation segment (Chunk {chunk_num}):
{conversation_text}

Summary:"""
        
        response = self.llm.generate([{"role": "user", "content": prompt}])
        return response.strip()
    
    def append_summary(self, workspace: str, conversation_id: str, summary: str, chunk_num: int):
        """Append a new summary to the summary file."""
        summary_file = self.get_summary_file(workspace, conversation_id)
        
        # Get first and last message timestamps from the chunk
        # For now, use current time as placeholder
        now = datetime.now()
        start_str = now.strftime("%Y-%m-%d %H:%M:%S")
        end_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        entry = f"\n## Chunk {chunk_num}: {start_str} → {end_str}\n\n{summary}\n"
        
        if summary_file.exists():
            content = summary_file.read_text()
            content = content.rstrip()
            summary_file.write_text(content + entry)
        else:
            header = f"# Conversation Summaries\n\nConversation: {conversation_id}\n"
            summary_file.write_text(header + entry)
    
    def ensure_summaries(self, workspace: str, conversation) -> bool:
        """Check and generate any missing summaries for a conversation."""
        conversation_id = conversation.id
        
        # Get existing chunk numbers
        existing = self.get_existing_chunks(workspace, conversation_id)
        
        # Get all message chunks
        message_chunks = self.get_message_chunks(conversation)
        total_chunks = len(message_chunks)
        
        # If no new chunks, return False
        if total_chunks <= len(existing):
            return False
        
        # Generate summaries for new chunks
        for i, chunk in enumerate(message_chunks):
            chunk_num = i + 1
            if chunk_num not in existing:
                summary = self.generate_summary(chunk, chunk_num)
                self.append_summary(workspace, conversation_id, summary, chunk_num)
                print(f"✅ Generated summary for chunk {chunk_num} of conversation {conversation_id}")
        
        return True

    def delete_summaries(self, workspace: str, conversation_id: str) -> bool:
        """Delete the summary file for a conversation."""
        summary_file = self.get_summary_file(workspace, conversation_id)
        if summary_file.exists():
            summary_file.unlink()
            print(f"🗑️ Deleted summaries for conversation {conversation_id}")
            return True
        return False