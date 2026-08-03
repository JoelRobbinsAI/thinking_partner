class CognitivePromptBuilder:
    def build(self, job):
        return (
            f"Object of attention:\n"
            f"{job.object_of_attention}\n\n"
            "Please reflect on the object of attention by "
            "answering exactly these three questions.\n\n"
            "1. What happened?\n\n"
            "2. What did I learn?\n\n"
            "3. What should change because of what I learned?\n\n"
            "Respond only with the completed reflection."
        )