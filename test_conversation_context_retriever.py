from backend.config import load_workspace
from backend.conversation_context_retriever import (
    ConversationContextRetriever,
)

workspace = load_workspace(
    "config/workspaces/clinical.yaml"
)

retriever = ConversationContextRetriever(
    workspace.workspace + "/conversations"
)

print(retriever.retrieve())