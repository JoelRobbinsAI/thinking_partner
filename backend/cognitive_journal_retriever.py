from backend.cognitive_journal import CognitiveJournal


class CognitiveJournalRetriever:
    """Retrieves context from both working and consolidated journals."""
    
    def __init__(self, base_name: str):
        """
        Initialize a retriever for a journal pair.
        
        Args:
            base_name: Base filename without extension (e.g., "conversation")
        """
        self.base_name = base_name
        self.journal = CognitiveJournal(base_name)
    
    def retrieve(self, working_limit: int = 10, consolidated_limit: int = 3) -> str:
        """
        Retrieve context from both working and consolidated journals.
        
        Args:
            working_limit: Number of recent working entries to include
            consolidated_limit: Number of recent consolidated entries to include
        
        Returns:
            Combined context string
        """
        working = self.journal.read_working(limit=working_limit)
        consolidated = self.journal.read_consolidated(limit=consolidated_limit)
        
        parts = []
        
        if consolidated:
            parts.append(f"## {self.base_name.title()} Consolidated Understanding\n\n{consolidated}")
        
        if working:
            parts.append(f"## {self.base_name.title()} Recent Reflections\n\n{working}")
        
        if not parts:
            return ""
        
        return "\n\n".join(parts)
    
    def retrieve_working_only(self, limit: int = 10) -> str:
        """Retrieve only working journal entries."""
        return self.journal.read_working(limit=limit)
    
    def retrieve_consolidated_only(self, limit: int = 5) -> str:
        """Retrieve only consolidated journal entries."""
        return self.journal.read_consolidated(limit=limit)