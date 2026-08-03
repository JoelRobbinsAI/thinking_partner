class CognitivePromptBuilder:
    def build(self, job):
        return (
            f"Object of attention:\n"
            f"{job.object_of_attention}\n\n"
            f"Question:\n"
            f"{job.question}\n"
        )