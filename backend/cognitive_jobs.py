from backend.cognitive_log import CognitiveLog
from backend.cognitive_prompt_builder import CognitivePromptBuilder

log = CognitiveLog()
builder = CognitivePromptBuilder()


class ConversationUnderstanding:
    job = "Conversation Understanding"
    object_of_attention = "Recent conversations"
    question = "What happened in recent conversations?"

    def run(self):
        prompt = builder.build(self)
        log.append(self.job, prompt)


class ProjectUnderstanding:
    job = "Project Understanding"
    object_of_attention = "Current projects"
    question = "What happened across the current projects?"

    def run(self):
        prompt = builder.build(self)
        log.append(self.job, prompt)


class UserUnderstanding:
    job = "User Understanding"
    object_of_attention = "The user"
    question = "What happened that taught me something about the user?"

    def run(self):
        prompt = builder.build(self)
        log.append(self.job, prompt)


class SelfImprovement:
    job = "Self Improvement"
    object_of_attention = "My own reasoning"
    question = "What happened in my own reasoning or behavior?"

    def run(self):
        prompt = builder.build(self)
        log.append(self.job, prompt)


class OpenContemplation:
    job = "Open Contemplation"
    object_of_attention = "Anything not already addressed"
    question = (
        "What important question should I be asking "
        "that hasn't already been addressed?"
    )

    def run(self):
        prompt = builder.build(self)
        log.append(self.job, prompt)


class Consolidation:
    job = "Consolidation"
    object_of_attention = "Working memory"
    question = "What should become part of long-term memory?"

    def run(self):
        prompt = builder.build(self)
        log.append(self.job, prompt)