# Thinking Partner

A personal AI Thinking Partner built around persistent conversations, modular cognition, reflection, and long-term memory.

## Vision

Thinking Partner is not intended to be another chatbot.

The goal is to build a persistent AI Thinking Partner that develops continuity over time through conversations, reflection, memory, and modular cognitive processes.

The emphasis is on building a clean, extensible architecture first, allowing increasingly sophisticated cognitive capabilities to be added over time.

## Core Philosophy

The Thinking Partner is built one architectural layer at a time.

Rather than attempting to build intelligence all at once, the project focuses on creating clean, modular components with clearly defined responsibilities. Each layer should be independently understandable, testable, and replaceable.

The long-term goal is for intelligence to emerge from the interaction of these components rather than from a single monolithic prompt or model.

Development follows a few guiding principles:

- Build one architectural layer at a time.
- Give every component a single responsibility.
- Prefer configuration over hardcoded behavior.
- Store important cognitive artifacts in human-readable Markdown.
- Build for long-term maintainability rather than short-term convenience.
- Commit small, working milestones before moving on.

## Current Architecture

The current architecture separates identity, conversation management, prompt construction, and language model interaction into independent components.

```text
                app.py
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
   Workspace  Conversation  PromptBuilder
        │          │          │
        └──────────┴──────────┘
                   │
                   ▼
                Messages
                   │
                   ▼
             OpenRouter LLM
```

### Workspace

Defines the conversational identity of a workspace.

Responsible for:

- Model selection
- System prompt
- Workspace directory

Workspace configuration is loaded from YAML, allowing different workspaces to use different models and behaviors without changing application code.

### ConversationManager

Responsible for:

- Creating conversations
- Listing conversations
- Loading conversations

Returns `Conversation` objects rather than raw Markdown.

### Conversation

Represents a single persistent conversation.

Responsible for:

- Conversation metadata
- Markdown storage
- Appending user messages
- Appending assistant messages
- Saving conversation history
- Converting conversation history into OpenAI/OpenRouter message format

The conversation itself serves as the system's working memory.

### PromptBuilder

Responsible for assembling the complete context presented to the language model.

Currently combines:

- Workspace system prompt
- Conversation history

Future versions will also include:

- Long-term memory
- Reflection summaries
- Additional contextual information

### LLM Layer

Provides a clean interface to OpenRouter.

Responsible for:

- Loading API credentials
- Sending messages
- Receiving responses

The LLM receives fully assembled context from the PromptBuilder rather than constructing prompts itself.

---

## Current Status

### Completed

- ✅ Workspace configuration
- ✅ Conversation management
- ✅ Persistent Markdown conversations
- ✅ Conversation loading
- ✅ Conversation history parsing
- ✅ PromptBuilder
- ✅ Workspace system prompts
- ✅ Conversation continuity
- ✅ OpenRouter integration
- ✅ Secure API key handling

### Current Milestone

Designing the reflection architecture that will generate long-term memory independently from the conversation loop.

### Next Milestone

Build the Reflection Agent and Memory architecture.

---

## Roadmap

### Phase 1 — Conversation Foundation ✅

- Workspace configuration
- Conversation persistence
- PromptBuilder
- OpenRouter integration
- Conversation continuity

### Phase 2 — Reflection Architecture 🚧

- Reflection Agent
- Reflection journal
- Memory extraction
- Long-term memory store
- PromptBuilder memory integration

### Phase 3 — Cognitive Architecture

- Background reflection loop
- Project memory
- Identity evolution
- Planning
- Semantic retrieval
- Multi-model cognition

---

## Future Architecture

```text
                        User
                          │
                          ▼
                    Conversation
                          │
          ┌───────────────┴───────────────┐
          │                               │
Conversation History              Workspace Identity
          │                               │
          └───────────────┬───────────────┘
                          │
                   PromptBuilder
                          ▲
                          │
                  Long-term Memory
                          ▲
                          │
                  Reflection Agent
                          ▲
                          │
                    Conversations
                          │
                          ▼
                     OpenRouter LLM
```

### Reflection Loop

The reflection system is intentionally separated from the conversation loop.

```text
Conversation
      │
      ▼
Reflection Agent
      │
      ▼
Reflection Journal
      │
      ▼
Memory Extraction
      │
      ▼
Long-term Memory
```

The conversation agent **reads** long-term memory but never writes it.

The reflection agent **writes** long-term memory but never participates directly in conversations.

This separation allows the Thinking Partner to distinguish between immediate conversational context (working memory) and durable knowledge accumulated over time.
