#!/usr/bin/env python3
"""
Thinking Partner - Conversation Interface
"""
import pyttsx3
import json
from pathlib import Path
from backend.config import load_workspace
from backend.conversation_manager import ConversationManager
from backend.llm import OpenRouterLLM
from backend.prompt_builder_with_journals import PromptBuilderWithJournals
from ddgs import DDGS

class ConversationApp:
    def __init__(self):
        """Initialize the app with workspace and conversation selection."""
        # Load the last used workspace from a state file
        self.state_file = Path(".thinking_partner_state.json")
        self.last_workspace = self._load_last_workspace()
        
        # Select workspace
        workspace_name = self._select_workspace()
        self.current_workspace_name = workspace_name
        
        # Load workspace config (returns a Workspace object)
        self.workspace = load_workspace(workspace_name)
        
        # Initialize components with ChromaDB support
        self.prompt_builder = PromptBuilderWithJournals(workspace_name=workspace_name)
        self.llm = OpenRouterLLM(model=self.workspace.model)
        self.tts_engine = pyttsx3.init()
        self.tts_enabled = True
        self.conversation_manager = ConversationManager(self.workspace)
        
        # Select conversation
        self.conversation_path = self._select_conversation()
        self.conversation = self._load_conversation_content()
        
        # Save last workspace
        self._save_last_workspace()
        self._show_status()
    
    def _load_last_workspace(self):
        """Load the last used workspace from state file."""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text(encoding="utf-8"))
                return data.get("last_workspace", "clinical")
            except:
                pass
        return "clinical"
    
    def _save_last_workspace(self):
        """Save the current workspace to state file."""
        data = {"last_workspace": self.current_workspace_name}
        self.state_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    
    def _get_available_workspaces(self):
        """Get list of available workspaces from config directory."""
        config_dir = Path("config/workspaces")
        if not config_dir.exists():
            return []
        return [f.stem for f in config_dir.glob("*.yaml")]
    
    def _select_workspace(self):
        """Interactive workspace selection."""
        workspaces = self._get_available_workspaces()
        
        if not workspaces:
            print("⚠️ No workspaces found. Creating default 'clinical'...")
            self._create_default_workspace("clinical")
            workspaces = ["clinical"]
        
        print("\n📁 Select Workspace:")
        print(f"   Last used: {self.last_workspace}")
        print()
        
        for i, ws in enumerate(workspaces, 1):
            marker = " (last)" if ws == self.last_workspace else ""
            print(f"   {i}. {ws}{marker}")
        
        print(f"   {len(workspaces) + 1}. Create new workspace")
        print()
        
        while True:
            try:
                choice = input(f"Choose workspace (1-{len(workspaces) + 1}, default={self.last_workspace}): ").strip()
                
                if not choice:
                    return self.last_workspace
                
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(workspaces):
                    return workspaces[choice_num - 1]
                elif choice_num == len(workspaces) + 1:
                    new_name = input("Enter new workspace name: ").strip()
                    if new_name:
                        self._create_default_workspace(new_name)
                        return new_name
                    else:
                        print("  Please enter a name.")
                        continue
                else:
                    print(f"  Please enter a number between 1 and {len(workspaces) + 1}")
            except ValueError:
                print("  Please enter a valid number.")
    
    def _get_conversations(self):
        """Get list of conversations in current workspace."""
        return self.conversation_manager.list_conversations()
    
    def _select_conversation(self):
        """Interactive conversation selection."""
        conversations = self._get_conversations()
        
        print(f"\n💬 Select Conversation (Workspace: {self.current_workspace_name}):")
        print()
        
        if not conversations:
            print("   No existing conversations.")
            print("   Starting a new conversation...")
            return self.conversation_manager.create_conversation()
        
        print("   Recent conversations:")
        for i, conv_path in enumerate(conversations[-10:], 1):
            try:
                display = conv_path.stem.replace("_", " at ")
                print(f"   {i}. {display}")
            except:
                print(f"   {i}. {conv_path.name}")
        
        print(f"   {len(conversations) + 1}. Start new conversation")
        print()
        
        while True:
            try:
                choice = input(f"Choose conversation (1-{len(conversations) + 1}, default=new): ").strip()
                
                if not choice:
                    print("   Starting new conversation...")
                    return self.conversation_manager.create_conversation()
                
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(conversations):
                    return conversations[choice_num - 1]
                elif choice_num == len(conversations) + 1:
                    print("   Starting new conversation...")
                    return self.conversation_manager.create_conversation()
                else:
                    print(f"  Please enter a number between 1 and {len(conversations) + 1}")
            except ValueError:
                print("  Please enter a valid number.")
    
    def _load_conversation_content(self):
        """Load the conversation content from the selected path."""
        if isinstance(self.conversation_path, Path):
            return self.conversation_manager.load_conversation(self.conversation_path)
        else:
            # It's a filepath (Path object) returned from create_conversation
            return self.conversation_manager.load_conversation(self.conversation_path)
    
    def _create_default_workspace(self, name):
        """Create a default workspace configuration."""
        config_dir = Path("config/workspaces")
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / f"{name}.yaml"
        
        if not config_path.exists():
            config_content = f"""# Workspace: {name}
model: openai/gpt-oss-120b
system_prompt: |
  You are a Thinking Partner, an AI assistant designed to help with thoughtful reflection and conversation.

  Your purpose is to:
  - Listen carefully and think deeply
  - Ask clarifying questions
  - Offer thoughtful perspectives
  - Help the user explore ideas

  Be curious, warm, and insightful. Focus on understanding rather than just answering.
  Always respond in English.

workspace_name: {name}
workspace_dir: workspaces/{name}
"""
            config_path.write_text(config_content, encoding="utf-8")
            print(f"✅ Created default workspace: {name}")
            
            # Create workspace directory
            workspace_dir = Path(f"workspaces/{name}")
            workspace_dir.mkdir(parents=True, exist_ok=True)
            (workspace_dir / "conversations").mkdir(parents=True, exist_ok=True)
            (workspace_dir / "cognitive_journals").mkdir(parents=True, exist_ok=True)
            (workspace_dir / "canonical").mkdir(parents=True, exist_ok=True)
    
    def _show_status(self):
        """Show current workspace and conversation status."""
        print(f"\n📁 Workspace: {self.current_workspace_name}")
        if hasattr(self.conversation, 'id'):
            print(f"💬 Conversation: {self.conversation.id}")
        print()
    
    def _list_workspaces(self):
        """List all available workspaces."""
        workspaces = self._get_available_workspaces()
        if workspaces:
            print("\n📂 Available workspaces:")
            for ws in workspaces:
                marker = "▶️ " if ws == self.current_workspace_name else "   "
                print(f"  {marker}{ws}")
        else:
            print("  No workspaces found.")
    
    def _switch_workspace(self, new_workspace):
        """Switch to a different workspace."""
        try:
            self.workspace = load_workspace(new_workspace)
        except FileNotFoundError:
            print(f"❌ Workspace '{new_workspace}' not found.")
            self._list_workspaces()
            return
        
        print(f"\n🔄 Switching from '{self.current_workspace_name}' to '{new_workspace}'...")

        # Switch workspace
        self.current_workspace_name = new_workspace
        self.prompt_builder = PromptBuilderWithJournals(workspace_name=new_workspace)
        self.workspace = load_workspace(new_workspace)
        self.llm = OpenRouterLLM(model=self.workspace.model)
        self.conversation_manager = ConversationManager(self.workspace)
        # TTS is already initialized in __init__, no need to reinitialize

        # Select conversation in new workspace
        self.conversation_path = self._select_conversation()
        self.conversation = self._load_conversation_content()
        self._save_last_workspace()
        self._show_status()
        print(f"✅ Switched to workspace '{new_workspace}'")
    
    def _start_new_conversation(self):
        """Start a new conversation in the current workspace."""
        print("\n🆕 Starting new conversation...")
        self.conversation_path = self.conversation_manager.create_conversation()
        self.conversation = self._load_conversation_content()
        self._show_status()
    
    def _list_conversations(self):
        """List conversations in current workspace."""
        conversations = self._get_conversations()
        if conversations:
            print(f"\n📋 Conversations in '{self.current_workspace_name}':")
            for conv_path in conversations[-10:]:
                try:
                    display = conv_path.stem.replace("_", " at ")
                    print(f"  - {display}")
                except:
                    print(f"  - {conv_path.name}")
        else:
            print(f"\n📭 No conversations in '{self.current_workspace_name}'")
    
    def _load_conversation_by_id(self, conv_id):
        """Load a specific conversation by ID or filename."""
        conversations = self._get_conversations()
        for conv_path in conversations:
            if conv_id in str(conv_path):
                self.conversation_path = conv_path
                self.conversation = self._load_conversation_content()
                print(f"\n✅ Loaded conversation: {conv_path.stem}")
                self._show_status()
                return
        print(f"\n❌ Conversation '{conv_id}' not found.")
    def _search_web(self, query):
        """Search DuckDuckGo and return results."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                return results
        except Exception as e:
            print(f"⚠️ Search error: {e}")
            return []
    def run(self):
        """Main conversation loop."""
        print("\n🧠 Thinking Partner")
        print("  Commands:")
        print("  /workspace [name]  - Switch workspaces")
        print("  /workspaces        - List available workspaces")
        print("  /new              - Start a new conversation")
        print("  /conversations    - List conversations in this workspace")
        print("  /load [id]        - Load a specific conversation")
        print("  /voice            - Toggle text-to-speech on/off")
        print("  /exit or /quit    - Exit")
        print()

        while True:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            # Natural language search triggers
            search_triggers = ["search for", "look up", "find information about", "what is", "tell me about"]
            is_search = False
            query = user_input

            for trigger in search_triggers:
                if user_input.lower().startswith(trigger):
                    query = user_input[len(trigger):].strip()
                    is_search = True
                    break

            if is_search and query:
                print(f"🔍 Searching: {query}")
                results = self._search_web(query)

                if not results:
                    print("  No results found.")
                    self.conversation.append_user(user_input)
                    self.conversation.append_assistant("I searched but found no results.")
                    continue

                print("\n📊 Search Results:")
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. {result.get('title', 'Untitled')}")
                    print(f"   {result.get('body', '')[:200]}...")
                    print(f"   🔗 {result.get('href', '')}")

                context = f"Search results for '{query}':\n"
                for result in results[:3]:
                    context += f"- {result.get('title')}: {result.get('body')[:150]}...\n"

                summary_prompt = f"Based on these search results, provide a concise, helpful answer to: '{query}'\n\nResults:\n{context}"
                print("\n🤔 Synthesizing answer...")
                summary = self.llm.generate([{"role": "user", "content": summary_prompt}])
                print(f"\n🌤️ Answer: {summary}")

                self.conversation.append_user(user_input)
                self.conversation.append_assistant(f"{summary}")
                continue
            # Voice toggle
            if user_input.lower() == "/voice":
                self.tts_enabled = not self.tts_enabled
                status = "on" if self.tts_enabled else "off"
                print(f"  Voice is now {status}")
                continue
            # Handle commands
            if user_input.lower() in ["/exit", "/quit"]:
                print("\n👋 Goodbye!")
                break

            if user_input.lower() == "/workspaces":
                self._list_workspaces()
                continue

            if user_input.startswith("/workspace"):
                parts = user_input.split()
                if len(parts) >= 2:
                    self._switch_workspace(parts[1])
                else:
                    print("  Usage: /workspace [name]")
                    self._list_workspaces()
                continue

            if user_input.lower() == "/new":
                self._start_new_conversation()
                continue

            if user_input.lower() == "/conversations":
                self._list_conversations()
                continue

            if user_input.startswith("/load"):
                parts = user_input.split()
                if len(parts) >= 2:
                    self._load_conversation_by_id(parts[1])
                else:
                    print("  Usage: /load [conversation_id]")
                continue

            if user_input.startswith("/search"):
                query = user_input[7:].strip()
                if not query:
                    print("  Usage: /search [query]")
                    continue

                print("🔍 Searching...")
                results = self._search_web(query)

                if not results:
                    print("  No results found.")
                    continue

                print("\n📊 Search Results:")
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. {result.get('title', 'Untitled')}")
                    print(f"   {result.get('body', '')[:200]}...")
                    print(f"   🔗 {result.get('href', '')}")

                context = f"Search results for '{query}':\n"
                for result in results[:3]:
                    context += f"- {result.get('title')}: {result.get('body')[:150]}...\n"

                summary_prompt = f"Based on these search results, provide a concise, helpful answer to: '{query}'\n\nResults:\n{context}"
                print("\n🤔 Synthesizing answer...")
                summary = self.llm.generate([{"role": "user", "content": summary_prompt}])
                print(f"\n🌤️ Answer: {summary}")

                self.conversation.append_user(f"/search {query}")
                self.conversation.append_assistant(f"{summary}")
                continue

            # Regular conversation
            self.conversation.append_user(user_input)
            messages = self.prompt_builder.build(self.workspace, self.conversation, user_input)
            print("🤔 Thinking...")
            response = self.llm.generate(messages)
            print(f"\nAssistant: {response}")
            self.conversation.append_assistant(response)

            # Speak the response
            if self.tts_enabled:
                self.tts_engine.say(response)
                self.tts_engine.runAndWait()
if __name__ == "__main__":
    app = ConversationApp()
    app.run()