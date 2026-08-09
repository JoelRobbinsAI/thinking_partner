from backend.cognitive_journal import CognitiveJournal
from backend.cognitive_journal_retriever import CognitiveJournalRetriever
from backend.cognitive_prompt_builder import CognitivePromptBuilder
from backend.cognitive_llm import CognitiveLLM
from backend.conversation_context_retriever import (
    ConversationContextRetriever,
)

builder = CognitivePromptBuilder()
llm = CognitiveLLM()

conversation_context = ConversationContextRetriever(
    "conversations"
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

conversation_journal_retriever = CognitiveJournalRetriever(
    "conversation.md"
)

project_journal_retriever = CognitiveJournalRetriever(
    "projects.md"
)

user_journal_retriever = CognitiveJournalRetriever(
    "user.md"
)

self_journal_retriever = CognitiveJournalRetriever(
    "self.md"
)

open_contemplation_journal_retriever = CognitiveJournalRetriever(
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

    def run(self, cycle_id):
        prompt = builder.build(
            self,
            [
                (
                    "Conversation Context",
                    conversation_context.retrieve(),
                ),
                (
                    "Conversation Journal",
                    conversation_journal_retriever.retrieve(),
                ),
            ],
        )

        reflection = llm.generate(prompt)

        conversation_journal.append(
            self.job,
            reflection,
            cycle_id,
        )


class ProjectUnderstanding:
    job = "Project Understanding"
    object_of_attention = "Current projects"

    reasoning_instructions = """
Prioritize Project Context.

Use the Conversation Journal as the primary source of evidence about
projects.

Use recent Project Journal entries as supporting working memory.

Focus on:

- Active projects.
- Progress.
- Obstacles.
- Next priorities.
"""

    def run(self, cycle_id):
        prompt = builder.build(
            self,
            [
                (
                    "Conversation Journal",
                    conversation_journal_retriever.retrieve(),
                ),
                (
                    "Project Journal",
                    project_journal_retriever.retrieve(),
                ),
            ],
        )

        reflection = llm.generate(prompt)

        project_journal.append(
            self.job,
            reflection,
            cycle_id,
        )


class UserUnderstanding:
    job = "User Understanding"
    object_of_attention = "The user"

    reasoning_instructions = """
Prioritize User Context.

Use the Conversation Journal as the primary source of evidence about
the user.

Use recent User Journal entries as supporting working memory.

Focus on:

- Goals.
- Preferences.
- Habits.
- Long-term patterns.
"""

    def run(self, cycle_id):
        prompt = builder.build(
            self,
            [
                (
                    "Conversation Journal",
                    conversation_journal_retriever.retrieve(),
                ),
                (
                    "User Journal",
                    user_journal_retriever.retrieve(),
                ),
            ],
        )

        reflection = llm.generate(prompt)

        user_journal.append(
            self.job,
            reflection,
            cycle_id,
        )


class SelfImprovement:
    job = "Self Improvement"
    object_of_attention = "My own reasoning"

    reasoning_instructions = """
Prioritize the Self Journal.

Use the Conversation Journal as evidence about actual interactions
and the quality of the system's behavior.

Use recent Self Journal entries as supporting working memory.

Focus on:

- Mistakes.
- Missed opportunities.
- Better reasoning strategies.
- Improvements to the system's own behavior.
"""

    def run(self, cycle_id):
        prompt = builder.build(
            self,
            [
                (
                    "Conversation Journal",
                    conversation_journal_retriever.retrieve(),
                ),
                (
                    "Self Journal",
                    self_journal_retriever.retrieve(),
                ),
            ],
        )

        reflection = llm.generate(prompt)

        self_journal.append(
            self.job,
            reflection,
            cycle_id,
        )


class OpenContemplation:
    job = "Open Contemplation"
    object_of_attention = "Anything not already addressed"

    reasoning_instructions = """
Use the available cognitive context.

Explore ideas, relationships, and questions that were not addressed
by the other cognitive jobs.

Remain grounded in the supplied artifacts.
"""

    def run(self, cycle_id):
        prompt = builder.build(
            self,
            [
                (
                    "Conversation Journal",
                    conversation_journal_retriever.retrieve(),
                ),
                (
                    "User Journal",
                    user_journal_retriever.retrieve(),
                ),
                (
                    "Project Journal",
                    project_journal_retriever.retrieve(),
                ),
                (
                    "Self Journal",
                    self_journal_retriever.retrieve(),
                ),
                (
                    "Open Contemplation Journal",
                    open_contemplation_journal_retriever.retrieve(),
                ),
            ],
        )

        reflection = llm.generate(prompt)

        open_contemplation_journal.append(
            self.job,
            reflection,
            cycle_id,
        )


class Consolidation:
    job = "Consolidation"
    object_of_attention = "Working memory"

    reasoning_instructions = """
Synthesize the four recent entries from this Cognitive Journal.

Preserve only information that is supported by the entries.

Identify the most important stable understanding that should
survive into the next working-memory cycle.

Do not introduce new facts, interpretations, questions,
recommendations, or topics that are not supported by the entries.
"""

    output_instructions = """
Write exactly one short paragraph synthesizing the four entries.

Do not use headings, bullet points, numbered lists, questions,
or additional sections.

The result should be concise enough to function as one working-memory
entry.
"""

    def run(self):
        journals = [
            (
                "Conversation Journal",
                conversation_journal,
            ),
            (
                "Project Journal",
                project_journal,
            ),
            (
                "User Journal",
                user_journal,
            ),
            (
                "Self Journal",
                self_journal,
            ),
            (
                "Open Contemplation Journal",
                open_contemplation_journal,
            ),
        ]

        for title, journal in journals:
            entries = journal.read_for_consolidation()

            if not entries:
                continue

            prompt = builder.build(
                self,
                [
                    (
                        title,
                        entries,
                    ),
                ],
            )

            reflection = llm.generate(prompt)

            journal.replace_recent(
                self.job,
                reflection,
            )