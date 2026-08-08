# Thinking Partner Architecture

This document describes the conceptual architecture of Thinking Partner.

Unlike `README.md`, which documents the current implementation, this document captures the long-term architectural vision and design philosophy of the project.

The architecture is intentionally allowed to remain ahead of the implementation.

---

# Fundamental Principle

Thinking Partner is not a chatbot.

It is a persistent cognitive system composed of two independent programs that communicate only through shared persistent artifacts.

Neither program directly invokes the other.

Instead, they communicate through conversations, journals, and long-term memory.

This separation is a permanent architectural constraint.

---

# Two Independent Programs

The system consists of two independently executable programs.

## 1. Conversation Interface

Purpose:

Communicate with the user.

Responsibilities:

* Receive user input.
* Assemble conversational context.
* Retrieve relevant long-term knowledge.
* Generate responses.
* Save conversations.

The Conversation Interface never performs cognition.

It never updates memory.

It only consumes knowledge.

---

## 2. Cognitive Engine

Purpose:

Develop understanding over time.

Responsibilities:

* Observe conversations.
* Reflect.
* Learn.
* Consolidate.
* Maintain long-term knowledge.

The Cognitive Engine never participates directly in conversations.

It only produces knowledge.

---

# Permanent Boundary

The two programs never invoke one another.

Communication occurs only through persistent artifacts.

```text
Conversation Interface
        │
        ▼
Conversation Archive

Conversation Interface
        │
        ▼
Canonical Memory
        ▲
        │
Cognitive Engine
```

This means:

* Either program may be started or stopped independently.
* Either program may be tested independently.
* Either program may eventually execute on different machines.
* Either program may use completely different language models.

The architecture intentionally avoids runtime coupling.

---

# Shared Persistent Artifacts

The programs communicate through persistent Markdown documents.

These artifacts form the shared cognitive environment of the system.

The persistent knowledge architecture consists of three conceptual layers:

```text
Conversation Archive
        │
        ▼
Cognitive Journals
        │
        ▼
Canonical Memory
```

The three layers have different purposes.

The Conversation Archive represents experience.

The Cognitive Journals represent active reflection and working cognition.

Canonical Memory represents current understanding.

---

# Conversation Archive

The Conversation Archive is the permanent record of interactions.

It represents experience rather than understanding.

Conversation records are not cognitive reflections.

They preserve what actually happened in conversations.

The Conversation Archive is never modified as part of normal cognitive processing.

It is read by Context Retrievers when cognitive processes need conversational evidence.

There is no requirement for a separate canonical Conversation Memory.

The conversation archive itself is the authoritative record of conversations.

When a conversation produces knowledge about the user, a project, the AI itself, or another meaningful subject, that knowledge can be reflected into the appropriate Cognitive Journal and eventually consolidated into Canonical Memory.

---

# Cognitive Journal Architecture

The Cognitive Journal is the working-memory layer of the Cognitive Engine.

Rather than maintaining one undifferentiated journal, cognitive reflections are partitioned according to their object of attention.

The system contains five Cognitive Journals:

* Conversation Journal
* User Journal
* Project Journal
* Self Journal
* Open Contemplation Journal

Each journal contains reflections produced by the corresponding cognitive process.

This allows each cognitive process to work with a small, relevant body of recent cognition rather than repeatedly processing the entire cognitive history.

---

# Conversation Journal

The Conversation Journal contains reflections about what happened in recent conversations.

Its purpose is to transform raw conversational experience into structured understanding.

Typical concerns include:

* Important events in conversations.
* Significant ideas.
* Decisions.
* Unresolved questions.
* Changes in direction.
* Information that may be relevant to other cognitive domains.

The Conversation Journal is working memory.

Stable information eventually moves into the appropriate Canonical Memory domain.

---

# User Journal

The User Journal contains reflections about the user.

Typical concerns include:

* Goals.
* Preferences.
* Habits.
* Patterns.
* Interests.
* Long-term tendencies.
* Important changes in the user's circumstances or direction.

The User Journal represents ongoing investigation and reflection.

Stable understanding eventually becomes part of Canonical User Memory.

---

# Project Journal

The Project Journal contains reflections about active projects.

Typical concerns include:

* Current projects.
* Project purpose.
* Progress.
* Obstacles.
* Decisions.
* Priorities.
* Dependencies.
* Emerging project direction.

The Project Journal represents working understanding of projects.

Stable project knowledge eventually becomes part of Canonical Project Memory.

---

# Self Journal

The Self Journal contains reflections about the Cognitive Engine itself.

Typical concerns include:

* Reasoning quality.
* Errors.
* Missed opportunities.
* Successful reasoning strategies.
* Behavioral patterns.
* Improvements to cognitive processes.
* Understanding of the system's own operation.

The Self Journal represents working self-understanding.

Stable understanding eventually becomes part of Canonical Self Memory.

---

# Open Contemplation Journal

The Open Contemplation Journal contains reflections that do not clearly belong to the other cognitive domains.

Its purpose is to provide space for exploratory cognition.

Typical concerns include:

* Unresolved ideas.
* Relationships between concepts.
* Unexpected observations.
* Questions not addressed by other cognitive processes.
* Potentially important ideas that have not yet found a permanent category.

Open contemplation provides a place for useful cognition to exist before its significance or destination becomes clear.

Information discovered here may eventually be consolidated into another canonical domain.

---

# Canonical Memory

Canonical Memory represents the current understanding of the system.

Unlike the Cognitive Journals, Canonical Memory is not a chronological record of reflection.

It consists of living documents describing what the system currently believes to be true or important.

Canonical Memory is periodically rewritten through consolidation.

The initial canonical domains are:

* User
* Projects
* Self

Additional canonical domains may be introduced if the architecture demonstrates a need for them.

---

# Canonical User Memory

Canonical User Memory contains the system's current understanding of the user.

It represents stable knowledge rather than individual reflections.

Examples include:

* Long-term goals.
* Persistent preferences.
* Established habits.
* Important patterns.
* Relevant relationships.
* Durable interests.

---

# Canonical Project Memory

Canonical Project Memory contains the system's current understanding of projects.

It represents the current state of project knowledge rather than the history of individual reflections.

Examples include:

* Project purpose.
* Current status.
* Major decisions.
* Known obstacles.
* Priorities.
* Important dependencies.
* Current direction.

---

# Canonical Self Memory

Canonical Self Memory contains the system's current understanding of itself.

It represents stable knowledge about the Cognitive Engine and its reasoning.

Examples include:

* Established reasoning patterns.
* Known weaknesses.
* Successful strategies.
* Important behavioral tendencies.
* Architectural self-understanding.
* Improvements that have become part of normal operation.

---

# Flow of Knowledge

Knowledge moves through progressively refined layers.

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

The Cognitive Engine performs the transformation from experience into reflection and eventually into canonical understanding.

The Conversation Interface reads canonical knowledge and relevant recent cognitive activity.

The Conversation Interface never modifies cognitive journals or canonical memory.

---

# Context Retrieval Architecture

One of the central design principles of Thinking Partner is that reasoning should never depend on a single monolithic prompt.

Instead, every language-model interaction is built from a collection of independent context sources.

Each source is responsible for retrieving one specific kind of information.

Together they assemble the context required for the current cognitive task.

This creates a library-like retrieval system rather than a single memory mechanism.

---

# Context Retrieval

A Context Retriever has one responsibility:

Retrieve one specific category of information.

Examples include:

* Conversation History.
* Conversation Journal.
* User Journal.
* Project Journal.
* Self Journal.
* Open Contemplation Journal.
* Canonical User Memory.
* Canonical Project Memory.
* Canonical Self Memory.
* Workspace Configuration.
* Future Context Providers.

Each retriever is independent and replaceable.

No retriever needs to understand how another retriever operates.

Retrievers never perform reasoning.

They only retrieve information.

---

# Context Builders

Context Builders assemble complete prompts by selecting and combining the appropriate Context Retrievers.

Two independent Context Builders exist.

## Conversation Prompt Builder

Constructs conversational prompts.

Possible sources include:

* Workspace Profile.
* System Prompt.
* Conversation History.
* Canonical User Memory.
* Canonical Project Memory.
* Canonical Self Memory.
* Recent relevant Cognitive Journal entries.

Its purpose is to construct the best possible conversational context.

---

## Cognitive Prompt Builder

Constructs prompts for cognitive processes.

Each cognitive process may require different evidence.

Possible sources include:

* Recent conversations.
* Conversation Journal.
* User Journal.
* Project Journal.
* Self Journal.
* Open Contemplation Journal.
* Canonical Memory.
* Active Projects.
* User knowledge.
* Previous reflections.

The Cognitive Prompt Builder determines how the selected context is assembled for the current cognitive process.

It does not retrieve information itself.

---

# Library Philosophy

Thinking Partner treats persistent knowledge as a library rather than a single memory.

Knowledge remains organized into independent collections.

Context Builders retrieve only the material needed for the current task.

As the system evolves, new Context Retrievers can be added without modifying either the Conversation Interface or the Cognitive Engine.

This makes context assembly modular, inspectable, and extensible.

The goal is not to build larger prompts.

The goal is to build better prompts by retrieving the right information from the right place at the right time.

---

# Cognitive Philosophy

The Cognitive Engine is a collection of scheduled cognitive processes.

Each process exists to answer one question about one object of attention.

Every process follows the same fundamental reasoning pattern:

1. What happened?
2. What did I learn?
3. What should change because of what I learned?

Only the object of attention and the relevant context change.

Current cognitive processes include:

* Conversation Understanding.
* Project Understanding.
* User Understanding.
* Self-Improvement.
* Open Contemplation.
* Consolidation.

Each process writes its reflection to the appropriate Cognitive Journal.

---

# Cognitive Processing Cycle

The Cognitive Engine operates as a repeated cycle.

```text
Scheduler
    │
    ▼
Select Cognitive Process
    │
    ▼
Retrieve Relevant Context
    │
    ▼
Build Cognitive Prompt
    │
    ▼
Generate Reflection
    │
    ▼
Write Reflection to Appropriate Journal
    │
    ▼
Next Cognitive Process
```

Each process should operate on a deliberately limited amount of context.

The Cognitive Engine should not repeatedly process the entire history of cognition.

Instead, it should retrieve recent and relevant entries from the appropriate journal.

This keeps prompts small, reduces unnecessary computation, and allows local models to perform focused cognitive operations.

---

# Consolidation

Consolidation is the process that transforms working cognition into canonical understanding.

Consolidation reads relevant Cognitive Journals and identifies information that appears:

* Stable.
* Repeated.
* Significant.
* Actionable.
* Appropriate for long-term retention.

It then updates the appropriate Canonical Memory documents.

Consolidation does not simply copy journal entries into memory.

It distills working reflections into current understanding.

The Cognitive Journals remain historical working cognition.

Canonical Memory remains the current state of knowledge.

---

# Memory Boundaries

The memory layers have deliberately different responsibilities.

Conversation Archive:

```text
What happened?
```

Cognitive Journals:

```text
What am I thinking about what happened?
```

Canonical Memory:

```text
What do I currently understand because of it?
```

This separation prevents raw experience, active reflection, and stable knowledge from becoming one undifferentiated memory store.

---

# Design Goal

The objective is not to build a chatbot with memory.

The objective is to build a persistent cognitive organism whose conversations are influenced by both:

* what it currently knows
* what it is currently thinking about

Long-term intelligence is expected to emerge from the interaction of independent cognitive processes operating over a persistent body of shared knowledge.

The architecture should allow increasingly sophisticated cognition to emerge without requiring increasingly large prompts.

Small, specialized cognitive processes should operate over small, relevant bodies of persistent knowledge.

---

# Long-Term Direction

The intended evolution is:

```text
Conversation Archive
        │
        ▼
Specialized Cognitive Journals
        │
        ▼
Focused Cognitive Processing
        │
        ▼
Consolidation
        │
        ▼
Partitioned Canonical Memory
        │
        ▼
Selective Context Retrieval
        │
        ▼
Better Conversation and Cognition
```

The architecture remains modular as new memory domains, Context Retrievers, cognitive processes, and language models are introduced.

The fundamental boundary remains unchanged:

**Conversation Interfaces communicate.**

**Cognitive Engines think.**

**Retrievers retrieve.**

**Prompt Builders assemble.**

**Language Models reason.**

**Cognitive Journals hold working cognition.**

**Canonical Memory holds current understanding.**

**Consolidation transforms reflection into knowledge.**
