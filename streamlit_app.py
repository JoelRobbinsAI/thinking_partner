import streamlit as st
import requests
import json
from pathlib import Path
import tempfile
import pygame
from gtts import gTTS
import os

st.set_page_config(page_title="Thinking Partner", page_icon="🧠", layout="wide")
st.title("🧠 Thinking Partner")

# Initialize session state
if "workspace" not in st.session_state:
    st.session_state.workspace = None
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
if "audio_playing" not in st.session_state:
    st.session_state.audio_playing = False
if "button_counter" not in st.session_state:
    st.session_state.button_counter = 0

API_URL = "http://localhost:8000"

# Sidebar
with st.sidebar:
    st.header("Workspace")
    
    try:
        response = requests.get(f"{API_URL}/workspaces")
        if response.status_code == 200:
            workspaces = response.json().get("workspaces", [])
        else:
            workspaces = []
    except:
        workspaces = []
    
    if workspaces:
        selected_workspace = st.selectbox(
            "Select Workspace",
            workspaces,
            index=workspaces.index(st.session_state.workspace) if st.session_state.workspace in workspaces else 0
        )
        if selected_workspace != st.session_state.workspace:
            st.session_state.workspace = selected_workspace
            st.session_state.conversation_id = None
            st.session_state.messages = []
            st.rerun()
    else:
        st.warning("No workspaces found. Make sure API is running.")
    
    st.divider()
    st.header("Conversations")
    
    if st.session_state.workspace:
        if st.button("+ New Conversation"):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "workspace": st.session_state.workspace,
                        "message": "New conversation"
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.conversation_id = data.get("conversation_id")
                    st.session_state.messages = []
                    st.success("New conversation created!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        
        conv_dir = Path("workspaces") / st.session_state.workspace / "conversations"
        if conv_dir.exists():
            conv_files = sorted(conv_dir.glob("*.md"), reverse=True)
            if conv_files:
                conv_options = ["Select a conversation"] + [f.stem for f in conv_files]
                selected_conv = st.selectbox(
                    "Load Conversation",
                    conv_options,
                    index=0
                )
                if selected_conv != "Select a conversation":
                    conv_id = selected_conv
                    if conv_id != st.session_state.conversation_id:
                        st.session_state.conversation_id = conv_id
                        st.session_state.messages = []
                        conv_file = conv_dir / f"{conv_id}.md"
                        if conv_file.exists():
                            content = conv_file.read_text()
                            lines = content.splitlines()
                            role = None
                            buffer = []
                            for line in lines:
                                if line.startswith("## User"):
                                    if role and buffer:
                                        st.session_state.messages.append({
                                            "role": role,
                                            "content": "\n".join(buffer).strip()
                                        })
                                    role = "user"
                                    buffer = []
                                elif line.startswith("## Assistant"):
                                    if role and buffer:
                                        st.session_state.messages.append({
                                            "role": role,
                                            "content": "\n".join(buffer).strip()
                                        })
                                    role = "assistant"
                                    buffer = []
                                elif role:
                                    buffer.append(line)
                            if role and buffer:
                                st.session_state.messages.append({
                                    "role": role,
                                    "content": "\n".join(buffer).strip()
                                })
                            st.rerun()
    
    st.divider()
    st.header("Settings")
    st.session_state.tts_enabled = st.toggle("Voice (gTTS)", value=st.session_state.tts_enabled)

# Main chat area
st.divider()

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and st.session_state.tts_enabled:
            st.session_state.button_counter += 1
            if st.button("🔊", key=f"speak_{st.session_state.button_counter}"):
                try:
                    tts = gTTS(text=msg["content"], lang="en", tld="co.uk", slow=False)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        tts.save(fp.name)
                        pygame.mixer.init()
                        pygame.mixer.music.load(fp.name)
                        pygame.mixer.music.play()
                except Exception as e:
                    st.error(f"Voice error: {e}")

# Chat input
if prompt := st.chat_input("What would you like to think about?"):
    if not st.session_state.workspace:
        st.error("Please select a workspace first.")
    else:
        search_triggers = ["search for", "look up", "find information about", "what is", "tell me about"]
        is_search = False
        query = prompt
        
        for trigger in search_triggers:
            if prompt.lower().startswith(trigger):
                query = prompt[len(trigger):].strip()
                is_search = True
                break
        
        if is_search and query:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Searching..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/search",
                            json={
                                "workspace": st.session_state.workspace,
                                "query": query
                            }
                        )
                        if response.status_code == 200:
                            data = response.json()
                            results = data.get("results", [])
                            if results:
                                result_text = f"**Search results for '{query}':**\n\n"
                                for i, result in enumerate(results, 1):
                                    result_text += f"{i}. **{result.get('title', 'Untitled')}**\n"
                                    result_text += f"   {result.get('body', '')[:300]}...\n"
                                    result_text += f"   🔗 {result.get('href', '')}\n\n"
                                
                                summary_response = requests.post(
                                    f"{API_URL}/chat",
                                    json={
                                        "workspace": st.session_state.workspace,
                                        "message": f"Based on these search results, provide a concise answer to: '{query}'\n\n{result_text}"
                                    }
                                )
                                if summary_response.status_code == 200:
                                    summary_data = summary_response.json()
                                    reply = summary_data.get("response", "No response")
                                    st.write(reply)
                                    st.session_state.messages.append({"role": "assistant", "content": reply})
                                else:
                                    st.write(result_text)
                                    st.session_state.messages.append({"role": "assistant", "content": result_text})
                            else:
                                reply = f"No results found for '{query}'."
                                st.write(reply)
                                st.session_state.messages.append({"role": "assistant", "content": reply})
                        else:
                            st.error(f"Search error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/chat",
                            json={
                                "workspace": st.session_state.workspace,
                                "message": prompt,
                                "conversation_id": st.session_state.conversation_id
                            }
                        )
                        if response.status_code == 200:
                            data = response.json()
                            reply = data.get("response", "No response")
                            st.session_state.conversation_id = data.get("conversation_id")
                            st.write(reply)
                            st.session_state.messages.append({"role": "assistant", "content": reply})
                            
                            if st.session_state.tts_enabled:
                                try:
                                    tts = gTTS(text=reply, lang="en", tld="co.uk", slow=False)
                                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                                        tts.save(fp.name)
                                        pygame.mixer.init()
                                        pygame.mixer.music.load(fp.name)
                                        pygame.mixer.music.play()
                                except Exception as e:
                                    pass
                            
                            st.rerun()
                        else:
                            st.error(f"API Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"Error: {e}")