from backend.cognitive_log import CognitiveLog
from backend.cognitive_prompt_builder import CognitivePromptBuilder
from backend.cognitive_llm import CognitiveLLM

log = CognitiveLog()
builder = CognitivePromptBuilder()
llm = CognitiveLLM()


class ConversationUnderstanding:
    job = "Conversation Understanding"
    object_of_attention = "Recent conversations"
    question = "What happened in recent conversations?"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class ProjectUnderstanding:
    job = "Project Understanding"
    object_of_attention = "Current projects"
    question = "What happened across the current projects?"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class UserUnderstanding:
    job = "User Understanding"
    object_of_attention = "The user"
    question = "What happened that taught me something about the user?"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class SelfImprovement:
    job = "Self Improvement"
    object_of_attention = "My own reasoning"
    question = "What happened in my own reasoning or behavior?"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class OpenContemplation:
    job = "Open Contemplation"
    object_of_attention = "Anything not already addressed"
    question = (
        "What important question should I be asking "
        "that hasn't already been addressed?"
    )

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class Consolidation:
    job = "Consolidation"
    object_of_attention = "Working memory"
    question = "What should become part of long-term memory?"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)