from pathlib import Path

from backend.memory_retriever import MemoryRetriever
from backend.canonical_retriever import CanonicalMemoryRetriever


class PromptBuilder:
    def __init__(self):
        self.memory_retriever = MemoryRetriever()
        self.canonical_retriever = CanonicalMemoryRetriever()

    def build(self, workspace, conversation):
        # Get existing memories
        memories = self.memory_retriever.get_memories(
            conversation
        )

        # Get canonical memory summary
        canonical_context = self.canonical_retriever.get_canonical_summary()

        # Read system prompt
        system_prompt = Path(
            workspace.system_prompt
        ).read_text()

        # Add memories if they exist
        if memories:
            memory_text = "\n\n".join(memories)

            system_prompt += (
                "\n\n"
                "Long-term memory:\n\n"
                f"{memory_text}"
            )

        # Add canonical memory if it exists and has content
        if canonical_context and "No canonical memory" not in canonical_context:
            system_prompt += (
                "\n\n"
                "Current Understanding from Canonical Memory:\n\n"
                f"{canonical_context}"
            )

        return conversation.to_messages(
            system_prompt=system_prompt
        )