from backend.prompt_builder import PromptBuilder
from backend.journal_embeddings import JournalEmbeddings

class PromptBuilderWithJournals(PromptBuilder):
    """Enhanced PromptBuilder that includes relevant journal entries."""
    
    def __init__(self, workspace_name="clinical"):
        super().__init__(workspace_name)
        self.journal_embeddings = JournalEmbeddings()
        # Embed any new journal entries on startup
        self.journal_embeddings.embed_all()
    
    def build_prompt(self, user_message, conversation_history=None):
        """Build prompt with relevant journal entries."""
        # Get the base prompt from parent
        prompt = super().build_prompt(user_message, conversation_history)
        
        # Search for relevant journal entries
        relevant_entries = self.journal_embeddings.search_all_journals(
            user_message, 
            n_results=3
        )
        
        if relevant_entries:
            journal_section = "\n\n## Recent Cognitive Journal Insights\n\n"
            journal_section += "Here are relevant thoughts from my reflective journals:\n\n"
            
            for entry in relevant_entries:
                journal_section += f"**From {entry['journal_name']} (Cycle {entry['cycle_id']}):**\n"
                journal_section += f"{entry['text'][:500]}...\n\n"
            
            # Insert journal section before the final prompt
            # Find where to insert (before "## Conversation" or at the end)
            if "## Conversation" in prompt:
                prompt = prompt.replace("## Conversation", journal_section + "\n## Conversation")
            else:
                prompt += journal_section
        
        return prompt