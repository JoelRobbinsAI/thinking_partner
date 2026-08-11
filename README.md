Here's the updated README with the RAG pipeline and performance improvements:

---

# Thinking Partner

A personal AI Thinking Partner built around persistent conversations, modular cognition, reflection, and long-term memory.

# Vision

Thinking Partner is not intended to be another chatbot.

Its purpose is to become a persistent AI Thinking Partner that develops continuity through conversations, reflection, and long-term knowledge.

Rather than relying on increasingly large prompts, the project explores whether long-term intelligence can emerge from independent cognitive processes operating over persistent knowledge.

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

Thinking Partner consists of two independent programs.

The **Conversation Interface** is responsible for interacting with the user.

The **Cognitive Engine** is responsible for developing long-term understanding.

Neither program invokes the other.

Instead, they communicate through persistent artifacts such as conversations, cognitive journals, and canonical memory.

Both programs remain:

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

It consumes knowledge but does not create or modify long-term cognitive knowledge.

### Workspace Management

The Conversation Interface supports multiple workspaces, each with its own:
- Configuration (model, system prompt)
- Conversation archive
- Cognitive journals
- Canonical memory

**Workspace selection** at startup:
- Interactive menu showing available workspaces
- Remembers the last used workspace
- Option to create new workspaces

**Conversation management** per workspace:
- List recent conversations
- Load existing conversations
- Start new conversations
- Persistent storage in Markdown files

**Runtime commands:**
- `/workspace [name]` - Switch workspaces during a conversation
- `/workspaces` - List available workspaces
- `/new` - Start a new conversation
- `/conversations` - List conversations in current workspace
- `/load [id]` - Load a specific conversation
- `/exit` or `/quit` - Exit the program

```text
User
   │
   ▼
Workspace Selection
   │
   ▼
Conversation Selection
   │
   ▼
PromptBuilder
   ├── Workspace Profile
   ├── System Prompt
   ├── RAG Context Retrievers
   │      ├── Semantic Search (ChromaDB)
   │      ├── Canonical Memory
   │      └── Journal Entries
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

### RAG Pipeline

The Conversation Interface uses a **Retrieval-Augmented Generation** pipeline for efficient context retrieval:

1. **Embeddings**: All memory (journals + canonical) is embedded using ChromaDB with the `all-MiniLM-L6-v2` model
2. **Semantic Search**: On each query, the system searches for the most relevant 2-3 chunks
3. **Focused Context**: Only the most relevant information is included in the prompt
4. **Latency Reduction**: Prompt size reduced from 2000+ tokens to 400-800 tokens
5. **Scalable**: Performance remains consistent as memory grows

### Workspace

Defines:

* Model
* System Prompt
* Workspace Directory

### ConversationManager

Responsible for:

* Creating conversations
* Listing conversations
* Loading conversations

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

### PromptBuilder

Constructs the complete prompt presented to the language model.

Uses RAG to retrieve relevant context from:
* Workspace profile
* System prompt
* Conversation history
* Canonical memory (semantic search)
* Journal entries (semantic search)

### CanonicalMemoryRetriever

Retrieves canonical memory for inclusion in conversation context using semantic search.

It:
* Uses ChromaDB embeddings for efficient retrieval
* Returns only the most relevant sections
* Never creates or modifies memory

### MemoryRetriever

Responsible only for reading persistent canonical knowledge.

It:

* Retrieves relevant memories.
* Returns them to the PromptBuilder.
* Never creates memory.
* Never modifies memory.

The Conversation Interface never writes to long-term memory.

---

## Program 2 — Cognitive Engine

Entry point:

```text
python -m backend.scheduler
```

The Cognitive Engine is responsible only for improving long-term understanding.

It never participates directly in conversations.

### Scheduler Modes

The scheduler supports three modes:

#### Production Mode
```bash
python -m backend.scheduler
```
- Real timing: 5 minutes between jobs, 4-hour cycle
- Consolidation at minutes 25, 30, 35, 40, 45 of hour 4
- Designed for continuous background operation
- Syncs to system clock for precise timing

#### Test Mode
```bash
python -m backend.scheduler --test
```
- Compressed timing: 3 seconds between jobs
- Complete 4-hour cycle in ~30 seconds
- For testing and validation

#### Development Mode
```bash
python -m backend.scheduler --dev
```
- No waiting between jobs
- For rapid iteration and debugging

### Scheduler Timing

**Hours 1-3:**
- Minute 0: Conversation Understanding → Conversation Journal
- Minute 5: Project Understanding → Project Journal
- Minute 10: User Understanding → User Journal
- Minute 15: Self-Improvement → Self Journal
- Minute 20: Open Contemplation → Open Journal
- Minute 25-59: Rest

**Hour 4:**
- Minute 0: Conversation Understanding → Conversation Journal
- Minute 5: Project Understanding → Project Journal
- Minute 10: User Understanding → User Journal
- Minute 15: Self-Improvement → Self Journal
- Minute 20: Open Contemplation → Open Journal
- Minute 25: Consolidate Conversation Journal → Update Canonical
- Minute 30: Consolidate Project Journal → Update Canonical
- Minute 35: Consolidate User Journal → Update Canonical
- Minute 40: Consolidate Self Journal → Update Canonical
- Minute 45: Consolidate Open Journal → Update Canonical

**After Hour 4:**
- Reset to Cycle 1, Hour 1
- Repeat indefinitely

The scheduler persists its state in `cognitive_state.json`, allowing it to resume from where it left off if interrupted.

### Scheduler Recovery

The scheduler includes robust recovery mechanisms:

- **Uneven state recovery**: If journals have different cycle counts (e.g., from stopping mid-cycle), the scheduler detects missing entries and reruns the appropriate jobs.
- **Verification after job runs**: Confirms each journal was written before marking a job complete.
- **State reconciliation**: On restart, reconciles journal states with the global cycle_id.
- **Continuous operation**: Runs indefinitely, handling interruptions gracefully.

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

The primary cognitive jobs use the same reflection structure:

1. What happened?
2. What did I learn?
3. What should change because of what I learned?

Each primary cognitive job writes one reflection to its corresponding Cognitive Journal.

Consolidation is a separate maintenance operation that synthesizes recent journal entries.

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

---

# Language Models

Thinking Partner uses two separate language models for different purposes:

## Conversation Interface
- Model: `mistralai/mistral-nemo:latest` (configurable per workspace)
- Purpose: Conversational responses
- Configured in workspace YAML
- Fast response times (~2-3 seconds)

## Cognitive Engine
- Model: `mistralai/mistral-nemo:latest`
- Purpose: Internal thinking and reflection
- Configured in `cognitive_llm.py`

This separation allows:
- Cost optimization (cheaper model for internal thinking)
- Performance optimization (better model for conversation)
- Independent upgrades

---

# Vector Memory (ChromaDB)

Thinking Partner uses ChromaDB for efficient semantic search:

- **Embeddings**: `all-MiniLM-L6-v2` (local, no API calls)
- **Collections**: Separate collections per workspace
- **Memory types**: Journals + Canonical memory
- **Retrieval**: Semantic search returns only the most relevant chunks
- **Persistence**: Vector database persists between sessions

---

# Canonical Memory

Canonical Memory represents the current understanding of the system.

It is fundamentally different from the Cognitive Journals.

The Cognitive Journals contain ongoing reflection.

Canonical Memory contains structured, living understanding.

Canonical Memory is organized categorically rather than chronologically.

The canonical domains are:

```text
User
Projects
Self
Open Knowledge
```

## Canonical Memory Structure

Each domain is stored as a Markdown file with predefined sections:

### User Memory (`user.md`)

```text
## Preferences
## Interests
## Background
## Goals
## Patterns
```

### Projects Memory (`projects.md`)

```text
## Current Projects
## Project State
## Priorities
## Relationships
```

### Self Memory (`self.md`)

```text
## Reasoning Patterns
## Strengths
## Weaknesses
## Improvements
```

### Open Knowledge Memory (`open_knowledge.md`)

```text
## Unresolved Questions
## Emerging Ideas
## Interesting Connections
```

## Canonical Update Process

After each Consolidation, the Canonical Memory Update job runs:

1. Reads the most recent Consolidation entry from each Cognitive Journal.
2. Presents the current canonical memory and the new consolidated reflection to the LLM.
3. The LLM determines if the canonical memory should be updated.
4. If updates are needed, the LLM specifies which sections to update and with what content.
5. The system applies the updates, preserving the structured format.

---

# Getting Started

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd thinking_partner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file with your OpenRouter API key:
```text
OPENROUTER_API_KEY=your-api-key-here
```

2. Configure workspaces in `config/workspaces/`

## Running

### Conversation Interface
```bash
python app.py
```

The app will present an interactive menu to select a workspace and conversation.

### Cognitive Engine
```bash
# Production mode (real timing)
python -m backend.scheduler

# Test mode (compressed timing)
python -m backend.scheduler --test

# Development mode (no waiting)
python -m backend.scheduler --dev
```

---

# Current Status

## Phase 1 — Conversation Interface ✅
- Workspace configuration
- Conversation management
- Persistent Markdown conversations
- PromptBuilder
- MemoryRetriever
- CanonicalMemoryRetriever
- Multi-turn conversation loop
- Interactive workspace selection with last-used memory
- Runtime workspace switching
- Conversation loading and listing

## Phase 2 — Cognitive Engine Foundation ✅
- Cognitive Scheduler with three modes
- Cognitive Jobs
- Cognitive Prompt Builder
- Cognitive LLM
- Independent execution
- End-to-end cognitive pipeline

## Phase 3 — Cognitive Working Memory ✅
- Five specialized Cognitive Journals
- Cognitive Journal persistence
- Recent-entry journal retrieval
- Dedicated Cognitive Journal Retrievers
- Each cognitive job writing to its corresponding journal
- Sequential cognitive job execution
- Four-cycle Consolidation process
- Rolling journal consolidation
- Consolidation boundary detection
- Scheduler state persistence and recovery

## Phase 4 — Canonical Memory ✅
- Canonical User Memory
- Canonical Project Memory
- Canonical Self Memory
- Canonical Open Knowledge
- Domain-specific canonical sections
- LLM-driven canonical update decisions
- Structured Markdown persistence
- Automatic canonical updates after consolidation

## Phase 5 — Production Scheduling ✅
- Time-based scheduler with production, test, and dev modes
- 5-minute job intervals
- 4-hour cycle with consolidation at minutes 25,30,35,40,45
- State persistence and recovery
- Background operation support
- Robust recovery from uneven journal states
- Cycle_id properly increments (1,2,3,4) and resets to 1
- Continuous indefinite operation

## Phase 6 — RAG Pipeline ✅
- ChromaDB integration for vector memory
- Semantic search across journals and canonical memory
- Embeddings with `all-MiniLM-L6-v2`
- Focused context retrieval (2-3 relevant chunks)
- Prompt size reduced from 2000+ to 400-800 tokens
- Latency reduced from 10-15s to 2-3s
- Workspace-aware collections
- Automatic embedding of new journal entries

---

# Future Work

## Phase 7 — Enhanced Capabilities 🚧
- DuckDuckGo search integration
- OpenWebUI/Conduit portability
- Voice interface (TTS/STT)
- Memory refinement and consolidation improvements

---

# Performance Benchmarks

| Metric | Before RAG | After RAG |
|--------|------------|-----------|
| **Prompt tokens** | 650-2000+ | 400-800 |
| **Response latency** | 10-15s | 2-3s |
| **Context retrieval** | All memory dumped | Semantic search |
| **Model** | GPT-OSS-120b | Mistral Nemo |
| **Scalability** | Degrades with memory growth | Remains consistent |

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

Consolidation distills working cognition.

Canonical Memory holds current understanding.

The Conversation Archive preserves experience.

The Cognitive Engine must remain grounded in persistent artifacts and must never manufacture experience simply because a plausible story would fit the current context.

Intelligence is expected to emerge from the interaction of independent cognitive processes operating over a persistent body of shared knowledge.

