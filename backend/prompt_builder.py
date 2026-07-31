from pathlib import Path


class PromptBuilder:
    def build(self, workspace, conversation, memories=None):
        if memories is None:
            memories = []

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