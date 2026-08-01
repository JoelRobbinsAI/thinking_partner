class ReflectionAgent:
    def reflect(self, conversation, llm):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a reflective AI. Read the conversation and "
                    "write a thoughtful reflection about what was learned, "
                    "what seems important, and what may deserve future "
                    "attention."
                ),
            }
        ]

        messages.extend(conversation.to_messages())

        return llm.generate(messages)