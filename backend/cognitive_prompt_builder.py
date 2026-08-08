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

        reasoning = getattr(
            job,
            "reasoning_instructions",
            "",
        ).strip()

        prompt = (
            "You are the Cognitive Engine of Thinking Partner, "
            "a persistent AI Thinking Partner system.\n\n"
            "Your primary purpose is to develop understanding that "
            "helps the system better assist its user.\n"
            "Your secondary purpose is to learn about your own "
            "reasoning and operation through reflection on your "
            "persistent cognitive artifacts.\n\n"
            "You learn only from persistent artifacts provided to you "
            "as context.\n"
            "Those artifacts represent the system's available memory "
            "and experience.\n\n"
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
            "Below are context documents containing the evidence "
            "available to you.\n\n"
            "Grounding Rules\n"
            "---------------\n"
            "Use only information supported by the supplied context.\n"
            "Do not invent events, projects, conversations, facts, "
            "people, decisions, or history.\n"
            "Do not infer that something happened merely because it "
            "would be plausible.\n"
            "Do not treat your previous generated reflections as "
            "facts unless they are supported by the underlying "
            "artifacts provided as context.\n"
            "If the available context does not contain enough evidence "
            "to answer a question, explicitly state that there is "
            "insufficient information.\n"
            "Treat the supplied context as the complete evidence "
            "available for this reflection.\n\n"
            "Context Documents:\n\n"
            f"{context}\n\n"
            "Reflect by answering exactly these three questions:\n\n"
            "1. What happened?\n\n"
            "2. What did I learn?\n\n"
            "3. What should change because of what I learned?\n\n"
            "Respond only with the completed reflection."
        )

        return prompt