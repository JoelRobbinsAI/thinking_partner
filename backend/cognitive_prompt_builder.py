class CognitivePromptBuilder:
    def build(self, job, context_sources):
        sections = []

        for title, content in context_sources:
            if content.strip():
                sections.append(
                    f"{title}\n"
                    f"{'-' * len(title)}\n"
                    f"{content}"
                )

        context = "\n\n".join(sections)

        reasoning = getattr(job, "reasoning_instructions", "").strip()

        prompt = (
            "You are the Cognitive Engine of the Thinking Partner.\n\n"
            f"Your current object of attention is:\n"
            f"{job.object_of_attention}\n\n"
        )

        if reasoning:
            prompt += (
                "Reasoning Instructions\n"
                "----------------------\n"
                f"{reasoning}\n\n"
            )

        prompt += (
            "Below are one or more context documents. "
            "Each document represents a different source of information.\n\n"
            "Use the context according to the reasoning instructions above.\n\n"
            "Context Documents:\n\n"
            f"{context}\n\n"
            "Reflect by answering exactly these three questions:\n\n"
            "1. What happened?\n\n"
            "2. What did I learn?\n\n"
            "3. What should change because of what I learned?\n\n"
            "Respond only with the completed reflection."
        )

        return prompt