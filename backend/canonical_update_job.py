import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from backend.canonical_memory import CanonicalMemory
from backend.cognitive_llm import CognitiveLLM

class CanonicalUpdateJob:
    """Updates canonical memory by merging consolidated insights with existing understanding."""
    
    def __init__(self):
        self.canonical = CanonicalMemory()
        self.llm = CognitiveLLM()
        self.journals_path = "cognitive_journals"
        
    def run(self):
        print("  → Starting canonical memory update...")
        
        journal_to_domain = {
            "conversation.md": "conversation",
            "user.md": "user",
            "projects.md": "projects",
            "self.md": "self",
            "open_contemplation.md": "open_knowledge"
        }
        
        for journal_file, domain in journal_to_domain.items():
            print(f"    → Processing {journal_file} -> {domain}")
            
            journal_path = os.path.join(self.journals_path, journal_file)
            
            consolidated = self._get_latest_consolidation(journal_path)
            if not consolidated:
                print(f"    → No consolidation found in {journal_file}, skipping")
                continue
                
            print(f"    → Found consolidation in {journal_file}")
            
            # Get current canonical content
            current_canonical = self.canonical.read_domain(domain)
            
            # Merge new consolidation with existing canonical memory
            merged = self._merge_with_canonical(domain, consolidated, current_canonical)
            
            if merged:
                print(f"  → Updating {domain} canonical memory...")
                self._apply_merged_update(domain, merged)
            else:
                print(f"  → No update needed for {domain}")
        
        print("  ✓ Canonical memory update complete")
    
    def _get_latest_consolidation(self, journal_path: str) -> str:
        """Get the most recent consolidated entry from a journal file."""
        filepath = Path(journal_path)
        
        if not filepath.exists():
            return None
        
        content = filepath.read_text(encoding="utf-8")
        if not content.strip():
            return None
        
        entries = content.split("\n# ")
        
        # Find the most recent Consolidation entry
        for entry in reversed(entries):
            if "Consolidation" in entry:
                # Extract the content (skip the header)
                lines = entry.split('\n')
                # Find where the actual content starts (after the header)
                content_start = 0
                for i, line in enumerate(lines):
                    if line.strip() and not line.startswith('#') and not line.startswith('Model:') and not line.startswith('Duration:'):
                        content_start = i
                        break
                return '\n'.join(lines[content_start:]).strip()
        
        return None
    
    def _merge_with_canonical(self, domain: str, consolidated: str, current_canonical: str) -> Optional[str]:
        """Ask LLM to merge consolidated insight with existing canonical memory."""
        
        print(f"    → Asking LLM to merge {domain}...")
        
        if not current_canonical or current_canonical.strip() == "":
            # No existing canonical memory — just use the consolidated content
            print(f"    → No existing canonical memory, using consolidated as initial")
            return consolidated
        
        prompt = f"""You are evolving canonical memory for a thinking partner system.

Domain: {domain}

EXISTING CANONICAL MEMORY:
{current_canonical}

NEW CONSOLIDATED INSIGHT:
{consolidated}

Your task: Evolve the canonical memory by merging the new insight with the existing understanding.

Guidelines:
1. Preserve what is still true and relevant from the existing memory
2. Update or refine anything that has changed
3. Add new insights that were not previously captured
4. Remove or deprecate anything that is no longer relevant
5. Keep the overall structure similar (sections, bullet points, etc.)
6. Write the updated content as a complete, coherent document

The result should be the UPDATED canonical memory content for this domain.
Do not include any explanations, headers, or meta-commentary.
Just output the updated content.

UPDATED CANONICAL MEMORY:"""
        
        response = self.llm.generate(prompt)
        
        print(f"    → Merge complete for {domain}")
        return response.strip()
    
    def _apply_merged_update(self, domain: str, merged_content: str):
        """Apply the merged content to canonical memory."""
        # Write the entire domain with the merged content
        file_path = os.path.join(self.canonical.base_path, self.canonical.domains[domain])
        
        # Add metadata header
        header = f"# {domain.title()} Memory\n\n"
        content = header + merged_content + f"\n\n---\n*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        
        with open(file_path, 'w') as f:
            f.write(content)