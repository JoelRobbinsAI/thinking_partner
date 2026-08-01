Thinking Partner

A personal AI Thinking Partner built around persistent conversations, modular cognition, reflection, and long-term memory.

Vision

Thinking Partner is not intended to be another chatbot.

Its purpose is to become a persistent AI Thinking Partner that develops continuity through conversations, reflection, and long-term knowledge.

Rather than relying on increasingly large prompts or models, the project explores whether long-term intelligence can emerge from cleanly separated cognitive processes operating over persistent knowledge.

Core Philosophy

The project is built one architectural layer at a time.

Rather than creating a single monolithic AI, the system is composed of small, specialized components with clearly defined responsibilities.

Every component should:

Have one responsibility.
Be independently understandable.
Be independently replaceable.
Leave inspectable artifacts.
Prefer configuration over hardcoded behavior.
Store persistent knowledge in human-readable Markdown.

The architecture intentionally separates conversation from learning.

System Architecture

Thinking Partner consists of two independent subsystems.

1. Conversation Interface

The Conversation Interface is responsible for interacting with the user.

It consumes context but never creates long-term knowledge.

User
   │
   ▼
PromptBuilder
   ├── Workspace Profile
   ├── System Prompt
   ├── Conversation History
   └── MemoryRetriever
            │
            ▼
      Long-Term Memory Store
            │
            ▼
      OpenRouter LLM
            │
            ▼
 Assistant Response
            │
            ▼
 Save Conversation
Components

Workspace

Defines:

Model
System Prompt
Workspace Directory

ConversationManager

Responsible for:

Creating conversations
Listing conversations
Loading conversations

Conversation

Represents one persistent conversation.

Responsible for:

Metadata
Markdown storage
User messages
Assistant messages
Saving conversation history
Producing OpenAI/OpenRouter message format

PromptBuilder

Constructs the complete prompt presented to the LLM.

Possible context includes:

Workspace profile
System prompt
Conversation history
Long-term memories
Future contextual information

MemoryRetriever

Responsible only for reading the memory store.

It:

Retrieves relevant memories.
Returns them to PromptBuilder.
Never modifies memory.
2. Cognitive Engine

The Cognitive Engine is an independent background system.

It does not participate in conversations.

Its purpose is to improve long-term knowledge.

Conversation Logs
        │
        ▼
 Reflection
        │
        ▼
 MemoryManager
        │
        ▼
 Long-Term Memory Store
Responsibilities

The Cognitive Engine may eventually include multiple specialized background workflows.

Examples include:

Reflection
Memory creation
Memory consolidation
Preference extraction
Identity refinement
Project organization
Relationship discovery

Each workflow has a single responsibility and operates independently.

Memory Architecture

The Conversation Interface and Cognitive Engine communicate only through the Long-Term Memory Store.

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

This establishes a strict architectural boundary.

The Conversation Interface reads memory.

The Cognitive Engine writes memory.

Neither subsystem directly controls the other.

Current Status
Completed
Workspace configuration
Conversation management
Persistent Markdown conversations
PromptBuilder
Conversation continuity
OpenRouter integration
Secure API key handling
Current Milestone

Building the foundational Conversation Interface.

Next Milestone

Designing the Long-Term Memory Store and Cognitive Engine.

Long-Term Roadmap
Phase 1 — Conversation Foundation ✅
Persistent conversations
PromptBuilder
Conversation continuity
Workspace profiles
Phase 2 — Memory Architecture 🚧
Long-Term Memory Store
MemoryRetriever
MemoryManager
Reflection journals
Phase 3 — Cognitive Engine
Background workflows
Reflection pipeline
Memory consolidation
Context orchestration
Multiple local cognitive models