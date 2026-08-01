from pathlib import Path

from backend.memory_manager import MemoryManager


class PromptBuilder:
    def __init__(self):
        self.memory_manager = MemoryManager()

    def build(self, workspace, conversation):
        memories = self.memory_manager.get_memories(
            conversation
        )

        system_prompt = Path(
            workspace.system_prompt
        ).read_text()

        if memories:
            memory_text = "\n\n".join(memories)

            system_prompt += (
                "\n\n"
                "Long-term memory:\n\n"
                f"{memory_text}"
            )

        return conversation.to_messages(
            system_prompt=system_prompt
        )