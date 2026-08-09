import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from backend.canonical_memory import CanonicalMemory
from backend.cognitive_llm import CognitiveLLM

class CanonicalUpdateJob:
    """Updates canonical memory based on consolidated journal entries."""
    
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
            print(f"    → Consolidation text: {consolidated[:100]}...")
            
            if domain == "conversation":
                self._process_conversation(consolidated)
            else:
                current_canonical = self.canonical.read_domain(domain)
                update = self._decide_update(domain, consolidated, current_canonical)
                
                if update["should_update"]:
                    print(f"  → Updating {domain} canonical memory...")
                    self._apply_update(domain, update)
                else:
                    print(f"  → No update needed for {domain}")
                    if update.get("reason"):
                        print(f"    Reason: {update['reason']}")
        
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
            if "Cycle: Consolidation" in entry or "Job: Consolidation" in entry:
                return entry.strip()
        
        return None
    
    def _decide_update(self, domain: str, consolidated: str, current_canonical: str) -> Dict:
        """Ask the LLM whether canonical memory should be updated."""
        
        print(f"    → Asking LLM about {domain} update...")
        
        prompt = f"""You are updating canonical memory for a thinking partner system.

Domain: {domain}

Current canonical memory:
{current_canonical if current_canonical else "(No existing canonical memory)"}

New consolidated reflection:
{consolidated}

Task: Determine if the canonical memory should be updated based on this new reflection.
Since this is the first update, you should almost certainly update the canonical memory.

YOU MUST RESPOND EXACTLY IN THIS FORMAT. DO NOT DEVIATE.

Example response:
UPDATE: yes
REASON: New information about the user's profession and tool usage
CHANGES:
SECTION: Background
CONTENT: The user is a Chinese medicine practitioner.
SECTION: Interests
CONTENT: The user is interested in discussing specific cases and refining reasoning workflows.

If no update is needed, respond with:
UPDATE: no
REASON: No new information that requires updating canonical memory

Now respond with exactly the format above.
"""
        
        response = self.llm.generate(prompt)
        
        print(f"    → LLM response for {domain}:")
        print(f"    {response[:300]}...")
        
        parsed = self._parse_update_response(response)
        print(f"    → Parsed result: should_update={parsed['should_update']}, changes={len(parsed['changes'])}")
        
        return parsed
    
    def _parse_update_response(self, response: str) -> Dict:
        """Parse the LLM response into an update decision."""
        result = {
            "should_update": False,
            "reason": "",
            "changes": []
        }
        
        lines = response.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('UPDATE:'):
                result["should_update"] = 'yes' in line.lower()
            elif line.startswith('REASON:'):
                result["reason"] = line[7:].strip()
            elif line.startswith('SECTION:'):
                if current_section and current_content:
                    result["changes"].append({
                        "section": current_section,
                        "content": '\n'.join(current_content).strip()
                    })
                current_section = line[8:].strip()
                current_content = []
            elif line.startswith('CONTENT:') and current_section:
                current_content.append(line[8:].strip())
            elif current_section and not line.startswith('---'):
                current_content.append(line)
                
        if current_section and current_content:
            result["changes"].append({
                "section": current_section,
                "content": '\n'.join(current_content).strip()
            })
            
        return result
    
    def _apply_update(self, domain: str, update: Dict):
        """Apply the update to canonical memory."""
        for change in update["changes"]:
            self.canonical.update_domain_section(
                domain,
                change["section"],
                change["content"]
            )
    
    def _process_conversation(self, consolidated: str):
        """Process conversation journal and distribute to multiple domains."""
        print(f"    → Processing conversation journal...")
        print(f"    → Consolidated text: {consolidated[:100]}...")
        
        current_canonical = self.canonical.read_domain("user")
        update = self._decide_update("user", consolidated, current_canonical)
        
        if update["should_update"]:
            print(f"  → Updating user canonical memory from conversation...")
            self._apply_update("user", update)
        else:
            print(f"  → No update needed for user from conversation")