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

Instead, they communicate only through persistent artifacts such as conversations, journals, and the Long-Term Memory Store.

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

It consumes context but never creates long-term knowledge.

```text
User
   │
   ▼
PromptBuilder
   ├── Workspace Profile
   ├── System Prompt
   ├── Context Retrievers
   │      ├── Conversation History
   │      └── MemoryRetriever
   │
   ▼
OpenRouter LLM
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

---

### PromptBuilder

Constructs the complete prompt presented to the language model.

Possible context includes:

* Workspace profile
* System prompt
* Conversation history
* Long-term memories
* Future contextual information

---

### MemoryRetriever

Responsible only for reading persistent memory.

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
Context Retrievers
        │
        ▼
Cognitive Prompt Builder
        │
        ▼
Cognitive LLM
        │
        ▼
Cognitive Log
        │
        ▼
MemoryManager
        │
        ▼
Long-Term Memory Store
```

### Scheduler

The Scheduler is the heartbeat of the Cognitive Engine.

It continuously monitors the clock and determines when cognitive work should occur.

Only one cognitive job is permitted to execute at a time.

The scheduler itself performs no reasoning. Its only responsibility is coordinating when cognitive jobs begin.

During development the scheduler currently uses short timed intervals for testing.

Future versions will execute jobs according to a production schedule.

---

### Cognitive Jobs

Each cognitive job observes a different object of attention while following the same reasoning pattern.

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

Only the object of attention changes.

---

### Cognitive Prompt Builder

Constructs prompts for cognitive work.

Its responsibility is completely separate from the PromptBuilder used by the Conversation Interface.

The Prompt Builder assembles the question a cognitive job should answer, while remaining independent of any language model implementation.

---

### Cognitive LLM

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

### Cognitive Log

The Cognitive Log is the working journal of the Cognitive Engine.

Every cognitive job records its reflection in the Cognitive Log.

The log is append-only and serves as temporary working memory until later consolidation into long-term memory.

Current implementation records placeholder reflections through the CognitiveLLM abstraction.

Future versions will record genuine model-generated reasoning.

---

### MemoryManager

MemoryManager maintains long-term knowledge.

Future responsibilities include:

* Creating memories
* Consolidating memories
* Updating canonical knowledge
* Removing obsolete information
* Organizing persistent knowledge

Unlike MemoryRetriever, MemoryManager never participates in conversations.

---

# Memory Architecture

The two programs communicate only through shared persistent knowledge.

```text
Conversation Interface
        │
        ▼
MemoryRetriever
        │
        ▼
Long-Term Memory Store
        ▲
        │
MemoryManager
        ▲
        │
Cognitive Engine
```

This establishes a strict architectural boundary.

The Conversation Interface only reads memory.

The Cognitive Engine only writes and maintains memory.

Neither program directly invokes the other.

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

---

## Current Milestone

Building contextual cognition.

The Cognitive Engine now performs genuine autonomous reflections using local language models.

Current work is focused on providing each cognitive job with the appropriate context so its reflections are grounded in evidence rather than generic reasoning.

---

## Next Milestone

Provide each cognitive job with meaningful context.

Examples include:

* Recent conversations
* Active projects
* User knowledge
* Recent cognitive log entries
* Long-term memory

Once each job has access to appropriate context, the scheduler will transition from accelerated testing intervals to its intended production schedule.
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
* Cognitive Log
* Independent execution

---

## Phase 3 — Memory Architecture 🚧

* Language-model reflections
* MemoryManager
* Long-Term Memory Store
* Memory consolidation
* Canonical memory documents

---

## Phase 4 — Autonomous Cognition

* Continuous background cognition
* Reflection pipeline
* Memory refinement
* Project understanding
* User understanding
* Self-improvement
* Multiple local cognitive models

---

# Design Principle

Thinking Partner is built from two independent programs.

The Conversation Interface communicates.

The Cognitive Engine thinks.

The Conversation Interface consumes knowledge.

The Cognitive Engine produces knowledge.

Neither program is responsible for the work of the other.

Intelligence is expected to emerge from the interaction of independent cognitive processes operating over a persistent body of shared knowledge.
