from backend.prompt_builder import PromptBuilder
from backend.journal_embeddings import JournalEmbeddings
from backend.canonical_retriever import CanonicalMemoryRetriever

class PromptBuilderWithJournals(PromptBuilder):
    def __init__(self, workspace_name="clinical"):
        super().__init__()
        self.workspace_name = workspace_name
        self.journal_embeddings = JournalEmbeddings(workspace_name=workspace_name)
        self.canonical_retriever = CanonicalMemoryRetriever(workspace_name=workspace_name)
        
        # Embed journal entries
        self.journal_embeddings.embed_all()
    
    def build(self, workspace, conversation, user_query=None):
        messages = super().build(workspace, conversation)
        
        if not user_query:
            return messages
        
        # Get relevant journal entries
        journal_results = self.journal_embeddings.search_all_journals(user_query, n_results=2)
        
        # Get relevant canonical sections
        canonical_results = self.canonical_retriever.search(user_query, n_results=2)
        
        # Combine into context
        context = ""
        
        if canonical_results:
            context += "\n\n## Relevant Long-term Memory\n\n"
            for entry in canonical_results:
                context += f"**From {entry['file']} - {entry['section']}:**\n{entry['text']}\n\n"
        
        if journal_results:
            context += "\n\n## Relevant Journal Reflections\n\n"
            for entry in journal_results:
                context += f"**From {entry['journal_name']} (Cycle {entry['cycle_id']}):**\n{entry['text'][:300]}...\n\n"
        
        if context:
            for msg in messages:
                if msg['role'] == 'system':
                    msg['content'] += context
                    break
        
        return messages