from backend.cognitive_log import CognitiveLog
from backend.cognitive_prompt_builder import CognitivePromptBuilder
from backend.cognitive_llm import CognitiveLLM

log = CognitiveLog()
builder = CognitivePromptBuilder()
llm = CognitiveLLM()


class ConversationUnderstanding:
    job = "Conversation Understanding"
    object_of_attention = "Recent conversations"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class ProjectUnderstanding:
    job = "Project Understanding"
    object_of_attention = "Current projects"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class UserUnderstanding:
    job = "User Understanding"
    object_of_attention = "The user"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class SelfImprovement:
    job = "Self Improvement"
    object_of_attention = "My own reasoning"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class OpenContemplation:
    job = "Open Contemplation"
    object_of_attention = "Anything not already addressed"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class Consolidation:
    job = "Consolidation"
    object_of_attention = "Working memory"

    def run(self):
        prompt = builder.build(self)
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)