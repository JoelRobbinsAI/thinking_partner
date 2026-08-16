
# Thinking Partner

A personal AI Thinking Partner with persistent conversations, modular cognition, reflection, and long-term memory.

---

## Vision

Thinking Partner is not a chatbot. It is a persistent cognitive system where intelligence emerges from the interaction of independent cognitive processes operating over a persistent body of shared knowledge.

---

## Core Features

- **Web UI** — Clean Streamlit interface accessible from any device on your network
- **Workspace Management** — Multiple workspaces with separate conversations, journals, and memory
- **Conversation History** — Persistent Markdown conversations with full context
- **Summary Buffer** — Automatic summarization of conversation history for long-term coherence
- **Voice** — Text-to-speech with British accent (gTTS)
- **Web Search** — DuckDuckGo integration with natural language triggers
- **Cognitive Engine** — Background reflection, journaling, and consolidation
- **Canonical Memory** — Structured long-term memory that evolves over time
- **RAG Pipeline** — Semantic search with ChromaDB embeddings
- **Delete Conversations** — Clean removal of conversations and their summaries

---

## Architecture

Thinking Partner consists of two independent programs that communicate through persistent artifacts:

| Program | Purpose |
|---------|---------|
| **Conversation Interface** (`app.py`) | Web UI and API server |
| **Cognitive Engine** (`backend/scheduler.py`) | Background reflection and learning |

**The Boundary:** Neither program invokes the other. They communicate through conversations, journals, and canonical memory.

---

## Quick Start

### 1. Clone and Install

```bash
git clone <repository-url>
cd thinking_partner
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

Create a `.env` file with your OpenRouter API key:

```
OPENROUTER_API_KEY=your-api-key-here
```

### 3. Run

**Terminal 1 — API Server:**
```bash
python app.py
```

**Terminal 2 — Web UI:**
```bash
streamlit run streamlit_app.py
```

### 4. Access

Open your browser to `http://localhost:8501` (or your network IP from another device).

---

## How It Works

### Conversation Context

The system builds context from four layers:

| Layer | Content | Purpose |
|-------|---------|---------|
| **System Prompt** | Your custom instructions | Behavior and tone |
| **Rolling Window** | Last 30 messages | Immediate coherence |
| **Summary Buffer** | Summaries of older chunks | Long-term thread continuity |
| **Retrieved Memory** | Journals + canonical (semantic search) | Cross-session knowledge |

### Cognitive Engine

Runs in the background, performing:

- **Reflection** — On conversations, projects, user, and self
- **Journaling** — Writing reflections to specialized journals
- **Consolidation** — Distilling journals into canonical memory

### Persistent Storage

All data is stored in human-readable Markdown:

```
workspaces/
├── [workspace]/
│   ├── conversations/       # Full conversation history
│   ├── [conversation].summary.md   # Summary buffer
│   ├── cognitive_journals/  # Working memory
│   └── canonical/           # Structured long-term memory
```

---

## Commands

### In the UI (Sidebar)

- **Select Workspace** — Switch between workspaces
- **+ New Conversation** — Start a fresh conversation
- **Load Conversation** — Select from existing conversations
- **🗑️ Delete** — Remove a conversation and its summary
- **Voice** — Toggle text-to-speech on/off

### Natural Language Search

The system automatically detects search queries with triggers like:
- `search for [query]`
- `look up [query]`
- `what is [query]`
- `tell me about [query]`

---

## Requirements

- Python 3.11+
- OpenRouter API key (for LLM access)
- Streamlit (for web UI)
- gTTS + pygame (for voice)

---

## Performance

| Metric | Value |
|--------|-------|
| Prompt tokens | 400-800 |
| Response latency | 2-3s |
| Context window | 128K (GPT-OSS-120B) |
| Model (default) | mistralai/mistral-nemo |

---

## Current Status

| Feature | Status |
|---------|--------|
| Workspace management | ✅ |
| Conversation management | ✅ |
| Web UI (Streamlit) | ✅ |
| RAG / ChromaDB | ✅ |
| Web search (DuckDuckGo) | ✅ |
| Voice (gTTS) | ✅ |
| Summary buffer | ✅ |
| Conversation deletion | ✅ |
| Cognitive Engine | ✅ |
| Canonical memory | ✅ |

---

## Design Philosophy

- **One responsibility per component** — Small, replaceable pieces
- **Persistent Markdown** — Human-readable, inspectable artifacts
- **Separation of communication and cognition** — Two independent programs
- **Intelligent context** — Retrieval-first, not brute-force

---
