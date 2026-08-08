# Thinking Partner

A personal AI Thinking Partner built around persistent conversations, modular cognition, reflection, and long-term memory.

## Vision

Thinking Partner is not intended to be another chatbot.

Its purpose is to become a persistent AI Thinking Partner that develops continuity through conversations, reflection, and long-term knowledge.

Rather than relying on increasingly large prompts or increasingly complex prompts, the project explores whether long-term intelligence can emerge from independent cognitive processes operating over persistent knowledge.

---

# Core Philosophy

The project is built one architectural layer at a time.

Rather than creating a single monolithic AI, the system is composed of small, specialized components with clearly defined responsibilities.

Every component should:

* Have one responsibility.
* Be independently understandable.
* Be independently replaceable.
* Leave inspectable artifacts.
* Prefer configuration over hardcoded behavior.
* Store persistent knowledge in human-readable Markdown.

The architecture intentionally separates communication from cognition.

---

# Architectural Boundary

Thinking Partner consists of two completely independent programs.

The **Conversation Interface** is responsible for interacting with the user.

The **Cognitive Engine** is responsible for developing long-term understanding.

Neither program ever invokes the other.

Instead, they communicate only through persistent artifacts such as conversations, journals, and canonical memory.

Both programs must always remain:

* Independently executable
* Independently testable
* Independently maintainable

This boundary is a permanent architectural constraint.

---

# System Architecture

## Program 1 — Conversation Interface

Entry point:

```text
app.py
```

The Conversation Interface is responsible only for communicating with the user.

It consumes knowledge but never creates or modifies long-term knowledge.

```text
User
   │
   ▼
PromptBuilder
   ├── Workspace Profile
   ├── System Prompt
   ├── Context Retrievers
   │      ├── Conversation History
   │      ├── Canonical User Memory
   │      ├── Canonical Project Memory
   │      ├── Canonical Self Memory
   │      └── Relevant Cognitive Activity
   │
   ▼
OpenRouter LLM
   │
   ▼
Assistant Response
   │
   ▼
Save Conversation
```

### Workspace

Defines:

* Model
* System Prompt
* Workspace Directory

---

### ConversationManager

Responsible for:

* Creating conversations
* Listing conversations
* Loading conversations

---

### Conversation

Represents one persistent conversation.

Responsible for:

* Metadata
* Markdown storage
* User messages
* Assistant messages
* Saving conversation history
* Producing OpenAI/OpenRouter message format

The Conversation Archive represents experience.

It is the authoritative record of what happened in conversations.

---

### PromptBuilder

Constructs the complete prompt presented to the language model.

Possible context includes:

* Workspace profile
* System prompt
* Conversation history
* Canonical memory
* Relevant recent cognitive activity
* Future contextual information

The PromptBuilder assembles context but does not perform cognition.

---

### MemoryRetriever

Responsible only for reading persistent knowledge.

It:

* Retrieves relevant canonical memories.
* Returns them to the PromptBuilder.
* Never creates memory.
* Never modifies memory.

The Conversation Interface never writes to long-term memory.

---

# Program 2 — Cognitive Engine

Entry point:

```text
python -m backend.cognitive_engine
```

The Cognitive Engine is responsible only for improving long-term understanding.

It never participates directly in conversations.

```text
Cognitive Engine
        │
        ▼
Scheduler
        │
        ▼
Cognitive Jobs
        │
        ▼
Context Retrievers
        │
        ▼
Cognitive Prompt Builder
        │
        ▼
Cognitive LLM
        │
        ▼
Specialized Cognitive Journal
        │
        ▼
Consolidation
        │
        ▼
Canonical Memory
```

---

## Scheduler

The Scheduler is the heartbeat of the Cognitive Engine.

It continuously monitors the clock and determines when cognitive work should occur.

Only one cognitive job is permitted to execute at a time.

The scheduler itself performs no reasoning.

Its only responsibility is coordinating when cognitive jobs begin.

During development the scheduler currently uses short timed intervals for testing.

Future versions will execute jobs according to a production schedule.

---

# Cognitive Jobs

Each cognitive job observes a different object of attention while following the same fundamental reasoning pattern.

Current jobs include:

* Conversation Understanding
* Project Understanding
* User Understanding
* Self-Improvement
* Open Contemplation
* Consolidation

Every cognitive job answers the same three questions:

1. What happened?
2. What did I learn?
3. What should change because of what I learned?

Only the object of attention and relevant context change.

Each cognitive job writes its reflection to its corresponding Cognitive Journal.

---

# Cognitive Journals

The Cognitive Engine uses specialized journals rather than one undifferentiated cognitive log.

The five working journals are:

* Conversation Journal
* User Journal
* Project Journal
* Self Journal
* Open Contemplation Journal

These journals are the working-memory layer of the Cognitive Engine.

Each journal contains reflections relevant to one cognitive domain.

The journals allow the Cognitive Engine to process small, focused bodies of recent cognition rather than repeatedly processing the entire cognitive history.

---

## Conversation Journal

Contains reflections about recent conversations.

It transforms conversational experience into structured understanding.

Possible content includes:

* Important events
* Significant ideas
* Decisions
* Unresolved questions
* Changes in direction
* Information relevant to other cognitive domains

---

## User Journal

Contains reflections about the user.

Possible content includes:

* Goals
* Preferences
* Habits
* Patterns
* Interests
* Long-term tendencies
* Important changes

---

## Project Journal

Contains reflections about active projects.

Possible content includes:

* Project purpose
* Current status
* Progress
* Obstacles
* Decisions
* Priorities
* Dependencies
* Emerging direction

---

## Self Journal

Contains reflections about the Cognitive Engine itself.

Possible content includes:

* Reasoning quality
* Mistakes
* Missed opportunities
* Successful reasoning strategies
* Behavioral patterns
* Cognitive improvements
* Understanding of the system's own operation

---

## Open Contemplation Journal

Contains reflections that do not clearly belong to another cognitive domain.

Possible content includes:

* Unresolved ideas
* Unexpected observations
* Relationships between concepts
* Questions not addressed elsewhere
* Ideas whose eventual significance or category is not yet clear

Open Contemplation provides a place for useful cognition before its permanent destination is known.

---

# Cognitive Prompt Builder

Constructs prompts for cognitive work.

Its responsibility is completely separate from the PromptBuilder used by the Conversation Interface.

The Cognitive Prompt Builder assembles the question a cognitive job should answer and combines only the context relevant to that job.

For example:

```text
Conversation Understanding
    ├── Recent Conversation
    └── Recent Conversation Journal

Project Understanding
    ├── Project Journal
    └── Relevant Canonical Project Memory

User Understanding
    ├── User Journal
    └── Canonical User Memory

Self-Improvement
    ├── Self Journal
    └── Relevant Cognitive Activity

Open Contemplation
    └── Selected available context
```

The exact context sources will evolve as the system develops.

The central principle is that cognitive jobs should operate on small, relevant context rather than the entire Cognitive Journal.

---

# Cognitive LLM

Provides the language-model interface for the Cognitive Engine.

Responsibilities include:

* Receiving cognitive prompts.
* Sending them to the selected language model.
* Returning generated reflections.
* Measuring execution time.
* Remaining independent of the cognitive jobs.

The current implementation uses local language models through Ollama.

Separating the language-model interface from the cognitive jobs allows different local or remote models to be substituted without modifying the architecture of the Cognitive Engine.

---

# Consolidation

Consolidation transforms working cognition into canonical understanding.

It reads relevant Cognitive Journals and identifies information that is:

* Stable
* Repeated
* Significant
* Actionable
* Appropriate for long-term retention

It then updates the appropriate Canonical Memory documents.

Consolidation does not simply copy journal entries into memory.

It distills working reflections into current understanding.

---

# Canonical Memory

Canonical Memory represents the current understanding of the system.

It is not a chronological journal.

It consists of living documents describing what the system currently understands.

The initial canonical domains are:

* User
* Projects
* Self

The Conversation Archive remains the authoritative record of conversations, so a separate canonical Conversation Memory is not currently required.

---

## Canonical User Memory

Contains stable understanding of the user.

Examples include:

* Long-term goals
* Persistent preferences
* Established habits
* Important patterns
* Relevant relationships
* Durable interests

---

## Canonical Project Memory

Contains the current understanding of projects.

Examples include:

* Project purpose
* Current status
* Major decisions
* Known obstacles
* Priorities
* Dependencies
* Current direction

---

## Canonical Self Memory

Contains stable understanding of the Cognitive Engine itself.

Examples include:

* Established reasoning patterns
* Known weaknesses
* Successful strategies
* Behavioral tendencies
* Architectural self-understanding
* Improvements that have become part of normal operation

---

# Memory Architecture

The system has three conceptual memory layers:

```text
Conversation Archive
        │
        ▼
Cognitive Journals
        │
        ▼
Canonical Memory
```

Their responsibilities are distinct.

### Conversation Archive

```text
What happened?
```

### Cognitive Journals

```text
What am I thinking about what happened?
```

### Canonical Memory

```text
What do I currently understand because of it?
```

This separation prevents experience, active reflection, and stable knowledge from becoming one undifferentiated memory store.

---

# Memory Flow

```text
Conversation
      │
      ▼
Conversation Journal
      │
      ├──────────────► User Journal
      │
      ├──────────────► Project Journal
      │
      ├──────────────► Self Journal
      │
      └──────────────► Open Contemplation Journal
                              │
                              ▼
                       Consolidation
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
        User Memory     Project Memory     Self Memory
```

The Cognitive Engine transforms experience into reflection and eventually into canonical understanding.

The Conversation Interface reads canonical knowledge and relevant recent cognitive activity.

The Conversation Interface never modifies cognitive journals or canonical memory.

---

# Context Retrieval Architecture

A Context Retriever has one responsibility:

Retrieve one specific category of information.

Possible retrievers include:

* Conversation History
* Conversation Journal
* User Journal
* Project Journal
* Self Journal
* Open Contemplation Journal
* Canonical User Memory
* Canonical Project Memory
* Canonical Self Memory
* Workspace Configuration
* Future Context Providers

Each retriever is independent and replaceable.

Retrievers never perform reasoning.

They only retrieve information.

---

# Current Status

## Completed

* ✅ Workspace configuration
* ✅ Conversation management
* ✅ Persistent Markdown conversations
* ✅ PromptBuilder
* ✅ MemoryRetriever
* ✅ Conversation continuity
* ✅ OpenRouter integration
* ✅ Secure API key handling
* ✅ Independent Conversation Interface
* ✅ Cognitive Engine
* ✅ Clock-based Scheduler
* ✅ Cognitive Jobs
* ✅ Universal Reflection Template
* ✅ Cognitive Prompt Builder
* ✅ Cognitive LLM
* ✅ Ollama integration
* ✅ Execution timing
* ✅ Cognitive Log
* ✅ End-to-end Cognitive Pipeline
* ✅ Recent-context Cognitive Log retrieval

---

# Current Milestone

## Organize Cognitive Working Memory

The Cognitive Engine has demonstrated that it can:

* Observe conversations.
* Build cognitive prompts.
* Generate reflections with a local model.
* Record reflections persistently.
* Retrieve recent cognitive activity.

The next implementation milestone is to replace the current single Cognitive Log with the five specialized Cognitive Journals:

* Conversation Journal
* User Journal
* Project Journal
* Self Journal
* Open Contemplation Journal

Each cognitive job will write only to its corresponding journal.

Each job will retrieve only the recent and relevant context required for its task.

This will reduce prompt size, reduce cognitive noise, and make local-model processing more efficient.

---

# Next Implementation Steps

### 1. Create the Five Cognitive Journals

Establish persistent Markdown storage for:

* Conversation reflections
* User reflections
* Project reflections
* Self reflections
* Open contemplation

---

### 2. Create Journal Retrievers

Create focused Context Retrievers capable of retrieving recent entries from each journal.

Retrievers should remain independent and reusable.

---

### 3. Update Cognitive Jobs

Modify each cognitive job so that it:

1. Retrieves its appropriate context.
2. Builds its focused prompt.
3. Generates one reflection.
4. Writes that reflection to its corresponding journal.

---

### 4. Implement Canonical Memory

Create the initial canonical memory domains:

* User
* Projects
* Self

---

### 5. Implement Consolidation

Create the Consolidation process that reads the specialized Cognitive Journals and distills stable understanding into Canonical Memory.

---

### 6. Update Conversation Context

Expand the Conversation Interface so it can selectively retrieve relevant canonical knowledge and recent cognitive activity.

---

### 7. Transition to Production Scheduling

Once the cognitive pipeline operates efficiently with focused context, transition the Scheduler from accelerated development intervals to its intended production schedule.

---

# Long-Term Roadmap

## Phase 1 — Conversation Interface ✅

* Persistent conversations
* PromptBuilder
* Conversation continuity
* Workspace profiles
* Memory retrieval

---

## Phase 2 — Cognitive Engine Foundation ✅

* Scheduler
* Cognitive Jobs
* Cognitive Prompt Builder
* Cognitive LLM
* Cognitive Log
* Independent execution
* End-to-end cognitive pipeline

---

## Phase 3 — Cognitive Working Memory 🚧

* Conversation Journal
* User Journal
* Project Journal
* Self Journal
* Open Contemplation Journal
* Specialized journal retrievers
* Focused cognitive context
* Job-specific context retrieval

---

## Phase 4 — Canonical Memory

* Canonical User Memory
* Canonical Project Memory
* Canonical Self Memory
* MemoryManager
* Memory consolidation
* Canonical knowledge refinement

---

## Phase 5 — Autonomous Cognition

* Continuous background cognition
* Reflection pipeline
* Selective context retrieval
* Memory refinement
* Project understanding
* User understanding
* Self-improvement
* Open contemplation
* Multiple local cognitive models
* Production scheduling

---

# Design Principle

Thinking Partner is built from two independent programs.

The Conversation Interface communicates.

The Cognitive Engine thinks.

The Conversation Interface consumes knowledge.

The Cognitive Engine produces knowledge.

Retrievers retrieve.

Prompt Builders assemble.

Language Models reason.

Cognitive Journals hold working cognition.

Canonical Memory holds current understanding.

Consolidation transforms reflection into knowledge.

Intelligence is expected to emerge from the interaction of independent cognitive processes operating over a persistent body of shared knowledge.
