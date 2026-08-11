"""
Canonical Memory Retriever

Provides access to canonical memory for the Conversation Interface.
Now uses semantic search via ChromaDB embeddings instead of dumping all files.
"""

from pathlib import Path
from typing import Dict, Optional, List
from backend.canonical_embeddings import CanonicalEmbeddings


class CanonicalMemoryRetriever:
    """Retrieves canonical memory for conversation context using RAG."""
    
    def __init__(self, workspace_name: str = "clinical", base_path: str = "backend/workspaces/cognitive/canonical"):
        """
        Initialize the retriever.
        
        Args:
            workspace_name: Name of the workspace (for ChromaDB collection)
            base_path: Path to the canonical memory directory (legacy, kept for compatibility)
        """
        self.workspace_name = workspace_name
        self.base_path = Path(base_path)
        self._cache = {}
        self._max_section_length = 150  # Max chars per section for summaries (legacy)
        
        # Initialize embeddings
        self.embeddings = CanonicalEmbeddings(workspace_name=workspace_name)
        self.embeddings.embed_all()  # Ensure all canonical sections are embedded
    
    def get_canonical_summary(self) -> str:
        """
        Legacy method - kept for compatibility.
        Returns a placeholder since we now use semantic search.
        """
        return "Canonical memory is now retrieved via semantic search based on your query."
    
    def search(self, query: str, n_results: int = 2) -> List[Dict]:
        """
        Search for relevant canonical sections using semantic search.
        
        Args:
            query: The user's query or message
            n_results: Number of relevant sections to retrieve
        
        Returns:
            List of relevant canonical sections with metadata
        """
        results = self.embeddings.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"$and": [{"type": "canonical"}, {"workspace": self.workspace_name}]}
        )
        
        formatted = []
        if results and results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted.append({
                    "text": results['documents'][0][i],
                    "file": results['metadatas'][0][i]['file'],
                    "section": results['metadatas'][0][i]['section'],
                    "distance": results['distances'][0][i] if results.get('distances') else None
                })
        
        return formatted
    
    def get_domain(self, domain: str) -> Optional[str]:
        """
        Get the full content of a specific canonical domain (legacy).
        Now returns a placeholder since we use embeddings.
        
        Args:
            domain: One of 'user', 'projects', 'self', 'open_knowledge'
        
        Returns:
            Full content of the domain, or None if not found
        """
        return f"Canonical domain '{domain}' is now retrieved via semantic search."
    
    def clear_cache(self):
        """Clear the internal cache."""
        self._cache = {}


# Convenience function for simple usage
def get_canonical_context() -> str:
    """
    Legacy function - kept for compatibility.
    Returns a placeholder.
    """
    return "Canonical memory is now retrieved via semantic search."