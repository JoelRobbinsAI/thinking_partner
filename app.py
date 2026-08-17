#!/usr/bin/env python3
"""
Thinking Partner - API Server
"""
import sys
sys.stdout.reconfigure(line_buffering=True)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional
from pathlib import Path
from ddgs import DDGS
import re
import yaml

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

prompt_builder = PromptBuilderWithJournals()
llm_client = OpenRouterLLM(model="mistralai/mistral-nemo:latest")
from backend.summary_generator import SummaryGenerator
summary_generator = SummaryGenerator(Path("workspaces"))

@app.post("/chat")
async def chat(request: ChatRequest):
    import traceback
    try:
        print(f"📥 Received: workspace={request.workspace}, conv_id={request.conversation_id}")
        
        ws = Workspace(
            name=request.workspace,
            model="mistralai/mistral-nemo:latest",
            system_prompt="You are a helpful thinking partner.",
            workspace=f"workspaces/{request.workspace}"
        )
        conv_mgr = ConversationManager(workspace=ws)
        
        if request.conversation_id:
            print("🔍 Loading existing...")
            conv_dir = Path("workspaces") / request.workspace / "conversations"
            files = list(conv_dir.glob(f"*{request.conversation_id}*.md"))
            if files:
                filepath = files[0]
            else:
                filepath = conv_dir / f"{request.conversation_id}.md"
            conv = conv_mgr.load_conversation(filepath)
        else:
            print("🆕 Creating new...")
            filepath = conv_mgr.create_conversation()
            print(f"   filepath: {filepath}")
            conv = conv_mgr.load_conversation(filepath)
            print(f"   conv.id: {conv.id}")
        
        print("💬 Appending user...")
        conv.append_user(request.message)
        
        print("🔨 Building prompt...")
        messages = prompt_builder.build(workspace=ws, conversation=conv)
        
        print("🤔 Generating...")
        full_response = llm_client.generate(messages)
        
        # Parse response and state
        response = full_response
        state_update = None
        
        if "STATE:" in full_response:
            parts = full_response.split("STATE:", 1)
            response = parts[0].strip()
            if response.startswith("RESPONSE:"):
                response = response.replace("RESPONSE:", "").strip()
            
            state_text = parts[1].strip()
            try:
                state_update = yaml.safe_load(state_text)
                if not isinstance(state_update, dict):
                    state_update = None
            except:
                state_update = None
        
        print("💾 Saving...")
        conv.append_assistant(response)
        
        if state_update:
            conv.update_state(state_update)
            print(f"📝 Updated conversation state")
        
        summary_generator.ensure_summaries(request.workspace, conv)

        return ChatResponse(response=response, conversation_id=conv.id)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
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
    query = request.get("query", "")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tts")
async def text_to_speech(request: dict):
    from gtts import gTTS
    import tempfile
    from pathlib import Path
    text = request.get("text", "")
    try:
        tts = gTTS(text=text, lang="en", tld="co.uk", slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_filename = Path(fp.name).name
            return {"audio_url": f"http://192.168.12.17:8000/audio/{audio_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    import tempfile
    from pathlib import Path
    from fastapi.responses import FileResponse
    audio_dir = Path(tempfile.gettempdir())
    filepath = audio_dir / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(path=filepath, media_type="audio/mpeg")

@app.delete("/conversation/{workspace}/{conv_id}")
async def delete_conversation(workspace: str, conv_id: str):
    """Delete a conversation and its summary file."""
    try:
        print(f"🗑️ Delete request: workspace={workspace}, conv_id={conv_id}")
        
        conv_dir = Path("workspaces") / workspace / "conversations"
        print(f"📁 Looking in: {conv_dir}")
        
        filepath = conv_dir / f"{conv_id}.md"
        
        if not filepath.exists():
            files = list(conv_dir.glob(f"{conv_id}*.md"))
            if files:
                filepath = files[0]
            else:
                raise HTTPException(status_code=404, detail=f"Conversation {conv_id} not found")
        
        content = filepath.read_text()
        match = re.search(r"id:\s*([a-f0-9\-]+)", content)
        if match:
            conversation_id = match.group(1)
        else:
            conversation_id = conv_id
        
        filepath.unlink()
        print(f"🗑️ Deleted conversation: {filepath}")
        
        summary_file = conv_dir.parent / f".{conversation_id}.summary.md"
        if summary_file.exists():
            summary_file.unlink()
            print(f"🗑️ Deleted summary: {summary_file}")
        
        return {"status": "success", "message": f"Deleted conversation {conv_id}"}
    except Exception as e:
        print(f"❌ Delete error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)