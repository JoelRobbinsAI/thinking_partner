from backend.prompt_builder import PromptBuilder
from backend.journal_embeddings import JournalEmbeddings
from backend.canonical_retriever import CanonicalMemoryRetriever
from pathlib import Path

class PromptBuilderWithJournals(PromptBuilder):
    def __init__(self, workspace_name="clinical"):
        super().__init__()
        self.workspace_name = workspace_name
        self.journal_embeddings = JournalEmbeddings(workspace_name=workspace_name)
        self.canonical_retriever = CanonicalMemoryRetriever(workspace_name=workspace_name)
        
        self.journal_embeddings.embed_all()
    
    def build(self, workspace, conversation, user_query=None):
        messages = super().build(workspace, conversation)
        
        # Include conversation summaries if they exist
        summary_file = Path("workspaces") / workspace.name / f".{conversation.id}.summary.md"
        summary_text = ""
        if summary_file.exists():
            summaries = summary_file.read_text()
            summary_text = f"\n\n**Previous Conversation Summaries:**\n{summaries}"
        
        # Include conversation state
        state_text = ""
        if hasattr(conversation, 'state') and conversation.state:
            state = conversation.state
            state_text = "\n\n## Current Conversation State\n"
            if state.get("current_topic"):
                state_text += f"- Topic: {state['current_topic']}\n"
            if state.get("intent"):
                state_text += f"- Intent: {state['intent']}\n"
            if state.get("user_mood"):
                state_text += f"- User Mood: {state['user_mood']}\n"
            if state.get("progress"):
                state_text += f"- Progress: {state['progress']}\n"
            if state.get("unresolved_questions"):
                state_text += f"- Unresolved Questions: {', '.join(state['unresolved_questions'])}\n"
            if state.get("decisions_made"):
                state_text += f"- Decisions Made: {', '.join(state['decisions_made'])}\n"
            if state.get("key_insights"):
                state_text += f"- Key Insights: {', '.join(state['key_insights'])}\n"
        
        if not user_query:
            if summary_text:
                for msg in messages:
                    if msg['role'] == 'system':
                        msg['content'] += summary_text
                        break
            if state_text:
                for msg in messages:
                    if msg['role'] == 'system':
                        msg['content'] += state_text
                        break
            return messages
        
        journal_results = self.journal_embeddings.search_all_journals(user_query, n_results=2)
        canonical_results = self.canonical_retriever.search(user_query, n_results=2)
        
        context = ""
        
        if canonical_results:
            context += "\n\n## Relevant Long-term Memory\n\n"
            for entry in canonical_results:
                context += f"**From {entry['file']} - {entry['section']}:**\n{entry['text']}\n\n"
        
        if journal_results:
            context += "\n\n## Relevant Journal Reflections\n\n"
            for entry in journal_results:
                context += f"**From {entry['journal_name']} (Cycle {entry['cycle_id']}):**\n{entry['text'][:300]}...\n\n"
        
        if summary_text:
            context += summary_text
        if state_text:
            context += state_text
        
        if context:
            for msg in messages:
                if msg['role'] == 'system':
                    msg['content'] += context
                    break
        
        return messages