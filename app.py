#!/usr/bin/env python3
"""
Thinking Partner - API Server
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional
from pathlib import Path
from ddgs import DDGS
app = FastAPI(title="Thinking Partner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    workspace: str
    conversation_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

from backend.workspace import Workspace
from backend.conversation_manager import ConversationManager
from backend.prompt_builder_with_journals import PromptBuilderWithJournals
from backend.llm import OpenRouterLLM

workspace_manager = Workspace(name="default", model="mistralai/mistral-nemo:latest", system_prompt="You are a helpful thinking partner.", workspace="default")
conversation_manager = ConversationManager(workspace=workspace_manager)
prompt_builder = PromptBuilderWithJournals()
llm_client = OpenRouterLLM(model="mistralai/mistral-nemo:latest")

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if request.conversation_id:
            conv_dir = Path("workspaces") / request.workspace / "conversations"
            files = list(conv_dir.glob(f"*{request.conversation_id}*.md"))
            if files:
                filepath = files[0]
            else:
                filepath = conv_dir / f"{request.conversation_id}.md"
            conv = conversation_manager.load_conversation(filepath)
        else:
            filepath = conversation_manager.create_conversation()
            conv = conversation_manager.load_conversation(filepath)
        
        conv.append_user(request.message)
        messages = prompt_builder.build(workspace=workspace_manager, conversation=conv)
        response = llm_client.generate(messages)
        conv.append_assistant(response)
        
        return ChatResponse(response=response, conversation_id=conv.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "online", "service": "Thinking Partner API"}

@app.get("/workspaces")
async def list_workspaces():
    workspaces_dir = Path("workspaces")
    if workspaces_dir.exists():
        workspaces = [d.name for d in workspaces_dir.iterdir() if d.is_dir()]
        return {"workspaces": workspaces}
    return {"workspaces": []}
@app.post("/search")
async def search(request: dict):
    from ddgs import DDGS
    query = request.get("query", "")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)