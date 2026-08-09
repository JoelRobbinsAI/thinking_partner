"""
Canonical Memory Retriever

Provides access to canonical memory for the Conversation Interface.
Retrieves summaries of all canonical domains for inclusion in conversation context.
"""

import os
from pathlib import Path
from typing import Dict, Optional, List
import re


class CanonicalMemoryRetriever:
    """Retrieves canonical memory for conversation context."""
    
    def __init__(self, base_path: str = "backend/workspaces/cognitive/canonical"):
        """
        Initialize the retriever.
        
        Args:
            base_path: Path to the canonical memory directory
        """
        self.base_path = Path(base_path)
        self._cache = {}
        self._max_section_length = 150  # Max chars per section for summaries
    
    def get_canonical_summary(self) -> str:
        """
        Get a concise summary of all canonical memory.
        
        Returns:
            Formatted string with summaries of all canonical domains
        """
        summaries = []
        
        # Load each canonical file
        domains = {
            "user": "User Understanding",
            "projects": "Projects Understanding", 
            "self": "Self Understanding",
            "open_knowledge": "Open Knowledge"
        }
        
        for filename, display_name in domains.items():
            content = self._load_canonical_file(filename)
            if content:
                summary = self._extract_summary(content, display_name)
                summaries.append(summary)
        
        if not summaries:
            return "No canonical memory has been developed yet."
        
        # Build the complete summary
        return self._format_summary(summaries)
    
    def _load_canonical_file(self, filename: str) -> Optional[str]:
        """Load a canonical memory file."""
        filepath = self.base_path / f"{filename}.md"
        
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading canonical file {filename}: {e}")
            return None
    
    def _extract_summary(self, content: str, domain: str) -> Dict:
        """
        Extract a summary from canonical content.
        
        Returns:
            Dict with domain name and summarized sections
        """
        sections = {}
        current_section = None
        current_content = []
        
        lines = content.split('\n')
        
        for line in lines:
            # Check for section headers (## Section Name)
            if line.startswith('## '):
                # Save previous section
                if current_section and current_content:
                    text = ' '.join(current_content).strip()
                    if text:
                        sections[current_section] = text[:self._max_section_length]
                
                # Start new section
                current_section = line.replace('## ', '').strip()
                current_content = []
            elif current_section:
                # Add to current section content
                if line.strip():
                    current_content.append(line.strip())
        
        # Save last section
        if current_section and current_content:
            text = ' '.join(current_content).strip()
            if text:
                sections[current_section] = text[:self._max_section_length]
        
        return {
            "domain": domain,
            "sections": sections
        }
    
    def _format_summary(self, summaries: List[Dict]) -> str:
        """Format summaries into a readable string."""
        result = ["## Current Understanding from Canonical Memory\n"]
        
        for summary in summaries:
            domain = summary["domain"]
            sections = summary["sections"]
            
            if not sections:
                continue
                
            result.append(f"### {domain}")
            
            for section_name, content in sections.items():
                if content:
                    result.append(f"**{section_name}:** {content}")
            
            result.append("")  # Empty line between domains
        
        return '\n'.join(result)
    
    def get_domain(self, domain: str) -> Optional[str]:
        """
        Get the full content of a specific canonical domain.
        
        Args:
            domain: One of 'user', 'projects', 'self', 'open_knowledge'
        
        Returns:
            Full content of the domain, or None if not found
        """
        filename = f"{domain}.md"
        content = self._load_canonical_file(filename)
        return content
    
    def clear_cache(self):
        """Clear the internal cache."""
        self._cache = {}


# Convenience function for simple usage
def get_canonical_context() -> str:
    """
    Get canonical memory context for conversation prompts.
    
    Returns:
        Formatted canonical memory summary
    """
    retriever = CanonicalMemoryRetriever()
    return retriever.get_canonical_summary()