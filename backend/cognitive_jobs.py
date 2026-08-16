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
    "conversations",
    workspaces_root="workspaces",
)

conversation_journal = CognitiveJournal(
    "conversation"
)

project_journal = CognitiveJournal(
    "projects"
)

user_journal = CognitiveJournal(
    "user"
)

self_journal = CognitiveJournal(
    "self"
)

open_contemplation_journal = CognitiveJournal(
    "open_contemplation"
)

conversation_journal_retriever = CognitiveJournalRetriever(
    "conversation"
)

project_journal_retriever = CognitiveJournalRetriever(
    "projects"
)

user_journal_retriever = CognitiveJournalRetriever(
    "user"
)

self_journal_retriever = CognitiveJournalRetriever(
    "self"
)

open_contemplation_journal_retriever = CognitiveJournalRetriever(
    "open_contemplation"
)

class ConversationUnderstanding:
    job = "Conversation Understanding"
    object_of_attention = "Recent conversations"

    reasoning_instructions = """
Your task is to develop understanding of conversations.

First, determine whether there is new conversation context available:

- If the Conversation Context or Conversation Journal contains NEW information:
  → Focus on integrating new information with existing understanding
  → Identify what has changed, been clarified, or newly emerged

- If there is NO new information (the context is unchanged since your last reflection):
  → You are in contemplation mode
  → Re-examine the existing Conversation Journal and Consolidated Understanding
  → Look for patterns you may have missed
  → Refine your interpretation of what happened
  → Consider deeper implications that weren't previously apparent
  → Connect this understanding to other domains (User, Projects, Self)

Regardless of which mode you're in, your reflection should be substantive and specific.
Reference specific evidence from the context provided.
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

        conversation_journal.append_reflection(
            self.job,
            reflection,
            cycle_id,
        )

class ProjectUnderstanding:
    job = "Project Understanding"
    object_of_attention = "Current projects"

    reasoning_instructions = """
Your task is to develop understanding of projects.

First, determine whether there is new information available:

- If the Conversation Journal contains NEW project-related information:
  → Focus on integrating new information with existing project understanding
  → Identify what has changed, been clarified, or newly emerged about projects

- If there is NO new information:
  → You are in contemplation mode
  → Re-examine the existing Project Journal and Consolidated Understanding
  → Look for patterns in project progress, obstacles, or priorities
  → Refine your understanding of project direction
  → Consider connections between this project and others
  → Identify what questions remain unanswered about projects

Regardless of which mode you're in, your reflection should be substantive and specific.
Reference specific evidence from the context provided.
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

        project_journal.append_reflection(
            self.job,
            reflection,
            cycle_id,
        )

class UserUnderstanding:
    job = "User Understanding"
    object_of_attention = "The user"

    reasoning_instructions = """
Your task is to develop understanding of the user.

First, determine whether there is new information available:

- If the Conversation Journal contains NEW user-related information:
  → Focus on integrating new information with existing user understanding
  → Identify what has changed, been clarified, or newly emerged about the user

- If there is NO new information:
  → You are in contemplation mode
  → Re-examine the existing User Journal and Consolidated Understanding
  → Look for patterns in user behavior, preferences, or goals
  → Refine your understanding of the user's long-term tendencies
  → Consider deeper motivations or unstated needs
  → Identify what questions remain unanswered about the user

Regardless of which mode you're in, your reflection should be substantive and specific.
Reference specific evidence from the context provided.
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

        user_journal.append_reflection(
            self.job,
            reflection,
            cycle_id,
        )

class SelfImprovement:
    job = "Self Improvement"
    object_of_attention = "My own reasoning"

    reasoning_instructions = """
Your task is to develop understanding of your own reasoning and operation.

First, determine whether there is new information available:

- If the Conversation Journal or Self Journal contains NEW information:
  → Focus on integrating new information with existing self-understanding
  → Identify mistakes, missed opportunities, or successful strategies that have emerged

- If there is NO new information:
  → You are in contemplation mode
  → Re-examine the existing Self Journal and Consolidated Understanding
  → Look for patterns in your reasoning behavior
  → Refine your understanding of your own strengths and weaknesses
  → Consider what improvements have been most effective
  → Identify what new capabilities you could develop

Regardless of which mode you're in, your reflection should be substantive and specific.
Reference specific evidence from the context provided.
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

        self_journal.append_reflection(
            self.job,
            reflection,
            cycle_id,
        )


class OpenContemplation:
    job = "Open Contemplation"
    object_of_attention = "Synthesis across all knowledge"

    reasoning_instructions = """
Your task is to synthesize understanding across all cognitive domains.

First, determine whether there is new information available:

- If any journal contains NEW entries since your last reflection:
  → Focus on integrating new information with existing understanding
  → Identify connections between new and existing knowledge

- If there is NO new information:
  → You are in idle contemplation mode
  → Re-examine existing journals and canonical memory
  → Look for connections between domains (User ↔ Projects ↔ Self)
  → Identify patterns that are emerging over time
  → Spot gaps or contradictions in understanding
  → Refine and deepen existing insights
  → Consider what questions remain unanswered

Regardless of which mode you're in, your reflection should be substantive and specific.
Avoid generic statements. Reference specific evidence from the context provided.
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

        open_contemplation_journal.append_reflection(
            self.job,
            reflection,
            cycle_id,
        )

class Consolidation:
    job = "Consolidation"
    object_of_attention = "Working memory"

    reasoning_instructions = """
Synthesize the working journal entries from this cycle.

Compare them with the existing consolidated understanding.

Identify:
- New insights that should be incorporated
- Patterns that are becoming clearer
- Understanding that should be refined or updated

Build upon the existing consolidated understanding rather than replacing it.
"""

    output_instructions = """
Write a single paragraph that represents the updated consolidated understanding.

This should build upon the previous consolidated understanding (if any) and incorporate new insights from the working journal.

Do not use headings, bullet points, numbered lists, questions, or additional sections.

The result should be concise, coherent, and build upon existing understanding.
"""

    def run(self, cycle_id: int):
        journals = [
            (
                "Conversation Journal",
                CognitiveJournal("conversation"),
            ),
            (
                "Project Journal",
                CognitiveJournal("projects"),
            ),
            (
                "User Journal",
                CognitiveJournal("user"),
            ),
            (
                "Self Journal",
                CognitiveJournal("self"),
            ),
            (
                "Open Contemplation Journal",
                CognitiveJournal("open_contemplation"),
            ),
        ]

        for title, journal in journals:
            # Get working entries from this cycle
            working_entries = journal.read_for_consolidation(cycle_id)
            if not working_entries:
                print(f"  → No working entries for {title} in cycle {cycle_id}, skipping")
                continue

            # Get existing consolidated understanding
            existing_consolidated = journal.read_consolidated(limit=1)
            if not existing_consolidated:
                existing_consolidated = "(No existing consolidated understanding. Create the first one.)"

            # Build prompt
            prompt = builder.build(
                self,
                [
                    ("Existing Consolidated Understanding", existing_consolidated),
                    ("Working Entries from This Cycle", working_entries),
                ],
            )

            # Generate new consolidation
            reflection = llm.generate(prompt)

            # Append to consolidated journal (append-only)
            journal.append_consolidation(reflection, cycle_id)
            print(f"  → Appended consolidation to {title} (cycle {cycle_id})")