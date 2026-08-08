from backend.cognitive_log import CognitiveLog
from backend.cognitive_prompt_builder import CognitivePromptBuilder
from backend.cognitive_llm import CognitiveLLM
from backend.conversation_context_retriever import (
    ConversationContextRetriever,
)
from backend.config import load_workspace

workspace = load_workspace(
    "config/workspaces/clinical.yaml"
)

log = CognitiveLog()
builder = CognitivePromptBuilder()
llm = CognitiveLLM()

conversation_context = ConversationContextRetriever(
    workspace.workspace + "/conversations"
)


class ConversationUnderstanding:
    job = "Conversation Understanding"
    object_of_attention = "Recent conversations"

    reasoning_instructions = """
Prioritize the Conversation Context.

Use the Cognitive Log only as supporting background.

Focus on understanding:

- What happened.
- What was learned.
- What should change because of what was learned.
"""

    def run(self):
        prompt = builder.build(
            self,
            [
                (
                    "Conversation Context",
                    conversation_context.retrieve(),
                ),
            ],
        )
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class ProjectUnderstanding:
    job = "Project Understanding"
    object_of_attention = "Current projects"

    reasoning_instructions = """
Prioritize Project Context.

Until Project Context exists, use the Cognitive Log as background.

Focus on:
- Active projects.
- Progress.
- Obstacles.
- Next priorities.
"""

    def run(self):
        prompt = builder.build(
            self,
            [
                (
                    "Cognitive Log",
                    log.read(),
                ),
            ],
        )
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class UserUnderstanding:
    job = "User Understanding"
    object_of_attention = "The user"

    reasoning_instructions = """
Prioritize User Context.

Until User Context exists, use the Cognitive Log as background.

Focus on:
- Goals.
- Preferences.
- Habits.
- Long-term patterns.
"""

    def run(self):
        prompt = builder.build(
            self,
            [
                (
                    "Cognitive Log",
                    log.read(),
                ),
            ],
        )
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class SelfImprovement:
    job = "Self Improvement"
    object_of_attention = "My own reasoning"

    reasoning_instructions = """
Prioritize the Cognitive Log.

Reflect on the quality of previous reasoning.

Look for:
- Mistakes.
- Missed opportunities.
- Better reasoning strategies.
"""

    def run(self):
        prompt = builder.build(
            self,
            [
                (
                    "Cognitive Log",
                    log.read(),
                ),
            ],
        )
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class OpenContemplation:
    job = "Open Contemplation"
    object_of_attention = "Anything not already addressed"

    reasoning_instructions = """
Use all available context.

Explore ideas, relationships, and questions that were not addressed by the other cognitive jobs.
"""

    def run(self):
        prompt = builder.build(
            self,
            [
                (
                    "Cognitive Log",
                    log.read(),
                ),
            ],
        )
        reflection = llm.generate(prompt)
        log.append(self.job, reflection)


class Consolidation:
    job = "Consolidation"
    object_of_attention = "Working memory"

    reasoning_instructions = """
Integrate information across all available context.

Look for:

- Stable knowledge.
- Repeated patterns.
- Information that should eventually become canonical memory.
  """

    def run(self):
        prompt = builder.build(
            self,
            [
                (
                    "Cognitive Log",
                    log.read(),
                ),
            ],
        )

        print(prompt)

        reflection = llm.generate(prompt)
        log.append(self.job, reflection)