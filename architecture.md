
Architecture

This document describes the conceptual architecture of Thinking Partner.

Unlike "README.md", which documents the current implementation, this document captures the long-term architectural vision and design philosophy of the project.

The architecture is intentionally allowed to remain ahead of the implementation.

---

Fundamental Principle

Thinking Partner is not a chatbot.

It is a persistent cognitive system composed of two independent programs that communicate only through shared persistent artifacts.

Neither program directly invokes the other.

Instead, they communicate through conversations, journals, and long-term memory.

This separation is a permanent architectural constraint.

---

Two Independent Programs

The system consists of two independently executable programs.

1. Conversation Interface

Purpose:

Communicate with the user.

Responsibilities:

- Receive user input.
- Assemble conversational context.
- Retrieve relevant long-term knowledge.
- Generate responses.
- Save conversations.

The Conversation Interface never performs cognition.

It never updates memory.

It only consumes knowledge.

---

2. Cognitive Engine

Purpose:

Develop understanding over time.

Responsibilities:

- Observe conversations.
- Reflect.
- Learn.
- Consolidate.
- Maintain long-term knowledge.

The Cognitive Engine never participates directly in conversations.

It only produces knowledge.

---

Permanent Boundary

The two programs never invoke one another.

Communication occurs only through persistent artifacts.

Conversation Interface
        │
        ▼
Conversation Archive

Conversation Interface
        │
        ▼
Long-Term Memory Store
        ▲
        │
Cognitive Engine

This means:

- Either program may be started or stopped independently.
- Either program may be tested independently.
- Either program may eventually execute on different machines.
- Either program may use completely different language models.

The architecture intentionally avoids runtime coupling.

---

Shared Persistent Artifacts

The programs communicate through persistent Markdown documents.

These artifacts include:

- Conversation Archive
- Cognitive Journal
- Canonical Memory

The artifacts form the shared cognitive environment of the system.

---

Context Retrieval Architecture

One of the central design principles of Thinking Partner is that reasoning should never depend on a single monolithic prompt.

Instead, every language-model interaction is built from a collection of independent context sources.

Each source is responsible for retrieving one specific kind of information.

Together they assemble the context required for the current cognitive task.

This creates a library-like retrieval system rather than a single memory mechanism.

---

Context Retrieval

A context retriever has one responsibility:

Retrieve one specific category of information.

Examples include:

- Conversation History
- Long-Term Memory
- Recent Cognitive Journal
- Active Projects
- Workspace Configuration
- Future Context Providers

Each retriever is independent and replaceable.

No retriever needs to understand how another retriever operates.

---

Context Builders

Context builders assemble complete prompts by selecting and combining the appropriate context retrievers.

Two independent context builders exist.

Conversation Prompt Builder

Constructs conversational prompts.

Possible sources include:

- Workspace Profile
- System Prompt
- Conversation History
- Canonical Memory
- Recent Cognitive Activity

Its purpose is to construct the best possible conversational context.

---

Cognitive Prompt Builder

Constructs prompts for cognitive processes.

Each cognitive process may require different evidence.

Possible sources include:

- Recent conversations
- Multiple conversation threads
- Canonical Memory
- Cognitive Journal
- Active Projects
- User knowledge
- Previous reflections

The Cognitive Prompt Builder determines which sources are relevant for the current cognitive process.

---

Library Philosophy

Thinking Partner treats persistent knowledge as a library rather than a single memory.

Knowledge remains organized into independent collections.

Context builders retrieve only the material needed for the current task.

As the system evolves, new context retrievers can be added without modifying either the Conversation Interface or the Cognitive Engine.

This makes context assembly modular, inspectable, and extensible.

The goal is not to build larger prompts.

The goal is to build better prompts by retrieving the right information from the right place at the right time.

---

Conversation Archive

The conversation archive is the permanent record of every interaction.

It is never modified after conversations are written.

It represents experience rather than understanding.

---

Cognitive Journal

The Cognitive Journal is the working memory of the Cognitive Engine.

Every scheduled cognitive process records structured reflections here.

The journal captures ongoing thought rather than permanent knowledge.

It is expected to evolve continuously.

---

Canonical Memory

Canonical Memory represents the current understanding of the system.

Unlike the Cognitive Journal, it is not a chronological history.

Instead, it consists of living documents describing the system's present understanding.

Examples include:

- User
- Projects
- Identity
- Preferences
- Relationships

These documents are periodically rewritten through consolidation.

They represent what the system currently believes rather than how it arrived there.

---

Flow of Knowledge

Knowledge always moves in one direction.

Conversation
        │
        ▼
Cognitive Journal
        │
        ▼
Canonical Memory

The Conversation Interface reads from Canonical Memory and recent Cognitive Journal entries to build conversational context.

The Cognitive Engine writes to both.

The Conversation Interface never modifies either.

---

Cognitive Philosophy

The Cognitive Engine is a collection of scheduled cognitive processes.

Each process exists to answer one question about one object of attention.

Every process follows the same reasoning pattern:

1. What happened?
2. What did I learn?
3. What should change because of what I learned?

Only the object of attention changes.

Current cognitive processes include:

- Conversation Understanding
- Project Understanding
- User Understanding
- Self-Improvement
- Open Contemplation
- Consolidation

Future processes may be added without altering the architecture.

Each new process simply receives its own schedule and maintains its own area of understanding.

---

Design Goal

The objective is not to build a chatbot with memory.

The objective is to build a persistent cognitive organism whose conversations are influenced by both:

- what it currently knows
- what it is currently thinking about

Long-term intelligence is expected to emerge from the interaction of independent cognitive processes operating over a persistent body of shared knowledge.