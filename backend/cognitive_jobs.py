from backend.cognitive_journal import CognitiveJournal
from backend.cognitive_prompt_builder import CognitivePromptBuilder
from backend.cognitive_llm import CognitiveLLM
from backend.conversation_context_retriever import (
    ConversationContextRetriever,
)
from backend.config import load_workspace


workspace = load_workspace(
    "config/workspaces/clinical.yaml"
)

builder = CognitivePromptBuilder()
llm = CognitiveLLM()

conversation_context = ConversationContextRetriever(
    workspace.workspace + "/conversations"
)

conversation_journal = CognitiveJournal(
    "conversation.md"
)

project_journal = CognitiveJournal(
    "projects.md"
)

user_journal = CognitiveJournal(
    "user.md"
)

self_journal = CognitiveJournal(
    "self.md"
)

open_contemplation_journal = CognitiveJournal(
    "open_contemplation.md"
)


class ConversationUnderstanding:
    job = "Conversation Understanding"
    object_of_attention = "Recent conversations"

    reasoning_instructions = """
Prioritize the Conversation Context.

Use the recent Conversation Journal entries as supporting background.

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
                (
                    "Conversation Journal",
                    conversation_journal.read_recent(),
                ),
            ],
        )
        reflection = llm.generate(prompt)
        conversation_journal.append(
            self.job,
            reflection,
        )


class ProjectUnderstanding:
    job = "Project Understanding"
    object_of_attention = "Current projects"

    reasoning_instructions = """
Prioritize Project Context.

Use recent Project Journal entries as supporting background.

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
                    "Project Journal",
                    project_journal.read_recent(),
                ),
            ],
        )
        print(prompt)
        reflection = llm.generate(prompt)
        project_journal.append(
            self.job,
            reflection,
        )


class UserUnderstanding:
    job = "User Understanding"
    object_of_attention = "The user"

    reasoning_instructions = """
Prioritize User Context.

Use recent User Journal entries as supporting background.

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
                    "User Journal",
                    user_journal.read_recent(),
                ),
            ],
        )
        reflection = llm.generate(prompt)
        user_journal.append(
            self.job,
            reflection,
        )


class SelfImprovement:
    job = "Self Improvement"
    object_of_attention = "My own reasoning"

    reasoning_instructions = """
Prioritize the Self Journal.

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
                    "Self Journal",
                    self_journal.read_recent(),
                ),
            ],
        )
        reflection = llm.generate(prompt)
        self_journal.append(
            self.job,
            reflection,
        )


class OpenContemplation:
    job = "Open Contemplation"
    object_of_attention = "Anything not already addressed"

    reasoning_instructions = """
Use the available cognitive context.

Explore ideas, relationships, and questions that were not addressed by the other cognitive jobs.
"""

    def run(self):
        prompt = builder.build(
            self,
            [
                (
                    "Conversation Journal",
                    conversation_journal.read_recent(),
                ),
                (
                    "User Journal",
                    user_journal.read_recent(),
                ),
                (
                    "Project Journal",
                    project_journal.read_recent(),
                ),
                (
                    "Self Journal",
                    self_journal.read_recent(),
                ),
                (
                    "Open Contemplation Journal",
                    open_contemplation_journal.read_recent(),
                ),
            ],
        )
        reflection = llm.generate(prompt)
        open_contemplation_journal.append(
            self.job,
            reflection,
        )


class Consolidation:
    job = "Consolidation"
    object_of_attention = "Working memory"

    reasoning_instructions = """
Integrate information across the Cognitive Journals.

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
                    "Conversation Journal",
                    conversation_journal.read_recent(),
                ),
                (
                    "User Journal",
                    user_journal.read_recent(),
                ),
                (
                    "Project Journal",
                    project_journal.read_recent(),
                ),
                (
                    "Self Journal",
                    self_journal.read_recent(),
                ),
                (
                    "Open Contemplation Journal",
                    open_contemplation_journal.read_recent(),
                ),
            ],
        )
        print(prompt)

        reflection = llm.generate(prompt)