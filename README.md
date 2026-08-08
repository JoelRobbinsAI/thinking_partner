# Thinking Partner

A personal AI Thinking Partner built around persistent conversations, modular cognition, reflection, and long-term memory.

# Vision

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

It consumes knowledge but never creates or modifies long-term cognitive knowledge.

```text
User
   │
   ▼
PromptBuilder
   ├── Workspace Profile
   ├── System Prompt
   ├── Context Retrievers
   │      ├── Conversation History
   │      ├── Canonical Memory
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

Workspace-specific conversation archives remain associated with the Conversation Interface.

The Cognitive Engine observes conversations through a separate system-level conversation source and does not inherit workspace-specific system prompts.

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

Responsible only for reading persistent canonical knowledge.

It:

* Retrieves relevant memories.
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
Focused Context
        │
        ▼
Cognitive Prompt Builder
        │
        ▼
Cognitive LLM
        │
        ▼
Specialized Cognitive Journals
        │
        ▼
Consolidation
        │
        ▼
Canonical Memory
```

The Cognitive Engine operates independently of the Conversation Interface.

---

# Scheduler

The Scheduler is the heartbeat of the Cognitive Engine.

It coordinates cognitive jobs sequentially.

The scheduler does not select jobs independently based on wall-clock slots. Each job completes before the next job begins.

The current development sequence is:

```text
Conversation Understanding
        ↓
Project Understanding
        ↓
User Understanding
        ↓
Self-Improvement
        ↓
Open Contemplation
        ↓
Cycle Complete
```

After every fourth complete cycle, Consolidation runs:

```text
Conversation Understanding
        ↓
Project Understanding
        ↓
User Understanding
        ↓
Self-Improvement
        ↓
Open Contemplation
        ↓
Consolidation
```

The current accelerated sequence is intended for development and testing.

The production scheduler will eventually introduce longer intervals between cognitive operations while preserving sequential processing.

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

Every cognitive job uses the same fundamental reflection structure:

1. What happened?
2. What did I learn?
3. What should change because of what I learned?

Only the object of attention and relevant evidence change.

Each primary cognitive job writes its reflection to its corresponding Cognitive Journal.

---

# Cognitive Journals

The Cognitive Engine uses specialized journals rather than one undifferentiated cognitive log.

The five working journals are:

* Conversation Journal
* User Journal
* Project Journal
* Self Journal
* Open Contemplation Journal

These journals form the working-memory layer of the Cognitive Engine.

Each journal contains reflections relevant to one cognitive domain.

The journals allow the Cognitive Engine to process small, focused bodies of recent cognition rather than repeatedly processing the entire cognitive history.

The previous single Cognitive Log model has been replaced by this specialized journal architecture.

`cognitive_log.py` remains in the repository temporarily as a legacy component and is no longer part of the active cognitive pipeline.

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

Conversation Understanding receives the system-level Conversation Archive as primary evidence and uses recent Conversation Journal entries as supporting working memory.

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

User Understanding receives relevant conversational evidence and recent User Journal entries.

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

Project Understanding receives relevant conversational evidence and recent Project Journal entries.

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

Self-Improvement receives evidence about actual system interactions together with recent Self Journal entries.

---

## Open Contemplation Journal

Contains reflections that do not clearly belong to another cognitive domain.

Possible content includes:

* Unresolved ideas
* Unexpected observations
* Relationships between concepts
* Questions not addressed elsewhere
* Ideas whose eventual significance or category is not yet clear

Open Contemplation receives the recent working context of the other cognitive journals and provides a place for useful cognition whose permanent destination is not yet known.

---

# Cognitive Journal

The reusable `CognitiveJournal` component provides the persistence mechanism for the specialized journals.

Each journal:

* Stores Markdown entries.
* Appends new reflections.
* Maintains its own independent file.
* Supports retrieval of recent entries.

The current implementation deliberately retrieves only a small number of recent entries.

This keeps cognitive prompts focused and reduces unnecessary local-model processing.

---

# Cognitive Journal Retriever

`CognitiveJournalRetriever` provides a dedicated retrieval interface for Cognitive Journals.

Each retriever is associated with one journal.

The cognitive jobs use these retrievers rather than directly managing journal-file contents.

This establishes a consistent separation:

```text
Cognitive Job
      │
      ▼
Journal Retriever
      │
      ▼
Recent Journal Entries
```

The job knows what information it needs.

The retriever knows how to obtain it.

---

# Cognitive Evidence Flow

The current working-memory architecture is intentionally hierarchical.

```text
Conversation Archive
        │
        ▼
Conversation Understanding
        │
        ▼
Conversation Journal
        │
        ├──────────────► Project Understanding
        │                       │
        │                       ▼
        │                Project Journal
        │
        ├──────────────► User Understanding
        │                       │
        │                       ▼
        │                  User Journal
        │
        └──────────────► Self-Improvement
                                │
                                ▼
                           Self Journal

Conversation Journal
User Journal
Project Journal
Self Journal
        │
        ▼
Open Contemplation
        │
        ▼
Open Contemplation Journal
```

This allows later cognitive jobs to build on earlier processing without repeatedly processing the entire Conversation Archive.

The design intentionally favors small evidence sets.

This reduces prompt size, local-model execution time, and cognitive noise.

---

# Global Conversation Source

The Cognitive Engine does not belong to any particular workspace.

It must not inherit the identity, system prompt, or specialized instructions of a workspace such as Clinical.

The Cognitive Engine now observes conversations through a system-level:

```text
conversations/
```

directory.

This prevents workspace-specific instructions from contaminating autonomous cognitive processing.

The Conversation Interface and Cognitive Engine therefore maintain separate responsibilities:

```text
Workspace Conversations
        │
        ▼
Conversation Interface


System Conversation Source
        │
        ▼
Cognitive Engine
```

The two programs remain independent even though they may operate over shared persistent artifacts.

---

# Cognitive Prompt Builder

Constructs prompts for cognitive work.

Its responsibility is completely separate from the PromptBuilder used by the Conversation Interface.

The Cognitive Prompt Builder:

* Establishes the global identity of the Cognitive Engine.
* Defines the current object of attention.
* Adds job-specific reasoning instructions.
* Assembles only the supplied context.
* Enforces artifact-based grounding.
* Requires the standard reflection structure.

The Cognitive Engine's global purpose is:

* Primarily to develop understanding that helps the system better assist its user.
* Secondarily to develop understanding of its own reasoning and operation.

The Cognitive Engine must learn from persistent artifacts rather than inventing history.

Its grounding rules explicitly prohibit inventing:

* Events
* Projects
* Conversations
* Facts
* People
* Decisions
* History

Generated reflections are not automatically treated as facts.

A model-generated reflection may become useful working evidence only when the architecture explicitly treats that artifact as evidence.

The Cognitive Prompt Builder therefore treats supplied artifacts as the complete available evidence for a reflection.

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

The current development scheduler runs Consolidation only after every fourth complete cognitive cycle.

The destination for Consolidation is temporary until Canonical Memory is implemented.

---

# Canonical Memory

Canonical Memory will represent the current understanding of the system.

It will not be a chronological journal.

It will consist of living documents describing what the system currently understands.

The initial canonical domains are:

* User
* Projects
* Self

The Conversation Archive remains the authoritative record of conversations, so a separate canonical Conversation Memory is not currently required.

Canonical Memory is the next major architectural layer after the Cognitive Working Memory layer is complete.

---

## Canonical User Memory

Will contain stable understanding of the user.

Examples include:

* Long-term goals
* Persistent preferences
* Established habits
* Important patterns
* Relevant relationships
* Durable interests

---

## Canonical Project Memory

Will contain the current understanding of projects.

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

Will contain stable understanding of the Cognitive Engine itself.

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

# Context Retrieval Architecture

A Context Retriever has one responsibility:

Retrieve one specific category of information.

Current retrieval components include:

* Conversation History
* Conversation Context
* Conversation Journal
* User Journal
* Project Journal
* Self Journal
* Open Contemplation Journal

Future retrieval components will include:

* Canonical User Memory
* Canonical Project Memory
* Canonical Self Memory
* Workspace Configuration
* Other specialized Context Providers

Retrievers never perform reasoning.

They only retrieve information.

---

# Grounding and Artifact Integrity

The Cognitive Engine is explicitly designed to learn from artifacts rather than construct fictional history.

This became an important architectural requirement during testing.

A small seed conversation produced reflections containing unsupported projects, patient information, research topics, and other details that were not present in the supplied evidence.

The architecture therefore treats grounding as a first-class concern.

The system must distinguish between:

```text
Observed Evidence
        ↓
Reflection
        ↓
Canonical Understanding
```

A reflection is an interpretation of evidence.

It is not automatically a new fact.

Future versions of the cognitive pipeline will further constrain reflection size, distinguish observation from interpretation, and prevent unsupported model-generated material from propagating between journals.

---

# Legacy Components

The original reflection subsystem has been retired.

The following legacy components are no longer part of the active architecture:

* `reflection_agent.py`
* `reflection_manager.py`
* Workspace `reflections/` directories

The specialized Cognitive Journal architecture replaces this earlier reflection mechanism.

`cognitive_log.py` also remains temporarily as a legacy file but is no longer used by the active Cognitive Engine pipeline.

Legacy components should be removed once their remaining dependencies have been verified.

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
* ✅ Sequential Cognitive Scheduler
* ✅ Cognitive Jobs
* ✅ Universal Reflection Structure
* ✅ Cognitive Prompt Builder
* ✅ Global Cognitive Engine identity
* ✅ Artifact-grounding rules
* ✅ Cognitive LLM
* ✅ Ollama integration
* ✅ Execution timing
* ✅ Five specialized Cognitive Journals
* ✅ Cognitive Journal persistence
* ✅ Recent-entry journal retrieval
* ✅ Dedicated Cognitive Journal Retrievers
* ✅ Each cognitive job writing to its corresponding journal
* ✅ Sequential cognitive job execution
* ✅ Fourth-cycle Consolidation trigger
* ✅ System-level Cognitive Engine conversation source
* ✅ Removal of Clinical workspace dependency from Cognitive Engine
* ✅ Legacy reflection subsystem retired

---

# Current Milestone

## Complete and Harden the Cognitive Working Memory Layer

The Cognitive Engine can now:

* Observe the system-level Conversation Archive.
* Build focused cognitive prompts.
* Generate reflections with a local model.
* Record reflections persistently.
* Maintain separate cognitive journals.
* Retrieve recent entries from each journal.
* Pass relevant journal context between cognitive jobs.
* Process cognitive jobs sequentially.
* Run Consolidation on a longer development cycle.

The architecture is now structurally capable of transforming conversational experience into specialized working cognition.

The remaining work in this layer is primarily about **grounding, evidence discipline, and efficiency**.

The local model must process small, relevant evidence sets without inventing unsupported history.

The next refinement is to make reflections shorter and more strictly evidence-bound so that unsupported interpretations do not propagate from one journal into another.

---

# Next Implementation Steps

### 1. Tighten Cognitive Reflection Grounding

Refine the Cognitive Prompt Builder and job instructions so reflections:

* Remain strictly grounded in supplied artifacts.
* Clearly distinguish observed information from interpretation.
* Avoid introducing unsupported history.
* Produce smaller, focused entries.
* Do not propagate invented details between journals.

This is the immediate development priority.

---

### 2. Validate Controlled Cognitive Propagation

Use deliberately seeded conversations containing known facts.

Run the complete cognitive sequence from a clean journal state and verify:

```text
Conversation
      ↓
Conversation Journal
      ↓
Project / User / Self
      ↓
Open Contemplation
```

The purpose is to verify that information propagates through the architecture without unsupported artifacts appearing.

---

### 3. Remove Remaining Legacy Components

After confirming that no active code depends on them:

* Remove `cognitive_log.py`.
* Remove other obsolete cognitive components.
* Clean generated artifacts such as `__pycache__` where appropriate.

---

### 4. Implement Canonical Memory

Create the initial canonical memory domains:

* User
* Projects
* Self

---

### 5. Implement Canonical Consolidation

Create the Consolidation process that reads the specialized Cognitive Journals and distills stable understanding into Canonical Memory.

Consolidation should transform working reflection into living knowledge rather than simply copying journal entries.

---

### 6. Update Conversation Context

Expand the Conversation Interface so it can selectively retrieve relevant canonical knowledge and recent cognitive activity.

---

### 7. Transition to Production Scheduling

Once the cognitive pipeline operates efficiently with focused context, transition the Scheduler from accelerated development execution to its intended production schedule.

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
* Independent execution
* End-to-end cognitive pipeline

---

## Phase 3 — Cognitive Working Memory 🚧

* Conversation Journal
* User Journal
* Project Journal
* Self Journal
* Open Contemplation Journal
* Recent-entry journal retrieval
* Specialized journal retrievers
* Focused cognitive context
* Job-specific context retrieval
* Global Conversation Archive retrieval
* Sequential cognitive processing
* Evidence-grounded reflection
* Reflection-size optimization

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

The Cognitive Engine must remain grounded in persistent artifacts and must never manufacture experience simply because a plausible story would fit the current context.

Intelligence is expected to emerge from the interaction of independent cognitive processes operating over a persistent body of shared knowledge.
