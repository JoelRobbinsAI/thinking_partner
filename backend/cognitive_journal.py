import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional


class CognitiveJournal:
    """Manages cognitive journals with working memory (rolling) and consolidated memory (append-only)."""
    
    def __init__(self, base_name: str, working_limit: int = 100):
        """
        Initialize a cognitive journal pair.
        
        Args:
            base_name: Base filename without extension (e.g., "conversation")
            working_limit: Maximum number of entries in working journal
        """
        self.base_name = base_name
        self.working_limit = working_limit
        self.working_path = Path(f"cognitive_journals/{base_name}_working.md")
        self.consolidated_path = Path(f"cognitive_journals/{base_name}_consolidated.md")
        
        # Ensure directory exists
        self.working_path.parent.mkdir(parents=True, exist_ok=True)
    
    def append_reflection(self, job: str, content: str, cycle_id: int) -> None:
        """Append a reflection to the working journal and purge if over limit."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = (
            f"# Cycle: {cycle_id} | Job: {job} | Time: {timestamp}\n\n"
            f"{content.strip()}\n\n"
            f"---\n"
        )
        
        # Read existing content
        existing = self._read_file(self.working_path)
        
        # Prepend new entry (most recent first)
        new_content = entry + existing
        
        # Parse entries and enforce limit
        entries = self._split_entries(new_content)
        if len(entries) > self.working_limit:
            entries = entries[:self.working_limit]
            new_content = "\n".join(entries) + "\n"
        
        self._write_file(self.working_path, new_content)
    
    def append_consolidation(self, content: str, cycle_id: int) -> None:
        """Append a consolidation to the consolidated journal (append-only)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = (
            f"# Consolidation Cycle: {cycle_id} | Time: {timestamp}\n\n"
            f"{content.strip()}\n\n"
            f"---\n"
        )
        
        # Read existing content
        existing = self._read_file(self.consolidated_path)
        
        # Append new entry (chronological order)
        new_content = existing + entry
        
        self._write_file(self.consolidated_path, new_content)

    def cycle_ids(self) -> List[int]:
        """Get all cycle IDs present in the working journal."""
        print(f"  → DEBUG: working_path = {self.working_path}")
        print(f"  → DEBUG: file exists = {self.working_path.exists()}")
        content = self._read_file(self.working_path)
        if not content:
            return []
        
        entries = self._split_entries(content)
        cycles = []
        for entry in entries:
            if not entry.strip():
                continue
            
            lines = entry.split('\n')
            for line in lines[:1]:
                if "Cycle:" in line:
                    try:
                        if "|" in line:
                            cycle_part = line.split("Cycle:")[1].split("|")[0].strip()
                            cycle_num = ''.join(c for c in cycle_part if c.isdigit())
                            if cycle_num:
                                cycles.append(int(cycle_num))
                                break
                        else:
                            cycle_str = line.split("Cycle:")[1].strip()
                            cycle_num = ''.join(c for c in cycle_str if c.isdigit())
                            if cycle_num:
                                cycles.append(int(cycle_num))
                                break
                    except (ValueError, IndexError):
                        pass
        
        return list(set(cycles))

    def _read_file(self, path: Path) -> str:
        """Read a file, returning empty string if it doesn't exist."""
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def _write_file(self, path: Path, content: str) -> None:
        """Write content to a file."""
        path.write_text(content.strip() + "\n", encoding="utf-8")

    def _split_entries(self, content: str) -> List[str]:
        """Split journal content into individual entries."""
        if not content.strip():
            return []
        
        # Split by "---" separators
        raw_entries = content.split("---\n")
        
        # Clean and filter empty entries
        entries = []
        for entry in raw_entries:
            entry = entry.strip()
            if entry:
                entries.append(entry + "\n\n---")
        
        return entries

    def read_working(self, limit: int = 10) -> str:
        """Read recent working journal entries."""
        content = self._read_file(self.working_path)
        if not content:
            return ""
        
        entries = self._split_entries(content)
        recent = entries[:limit]  # Most recent first
        
        return "\n".join(recent)
    
    def read_consolidated(self, limit: int = 5) -> str:
        """Read recent consolidated journal entries."""
        content = self._read_file(self.consolidated_path)
        if not content:
            return ""
        
        entries = self._split_entries(content)
        recent = entries[-limit:] if len(entries) > limit else entries  # Most recent last
        
        return "\n".join(recent)
    
    def read_for_consolidation(self, cycle_id: int) -> str:
        """Read working entries from a specific cycle for consolidation."""
        content = self._read_file(self.working_path)
        if not content:
            return ""
        
        entries = self._split_entries(content)
        
        # Find entries from this cycle
        cycle_entries = []
        for entry in entries:
            if f"Cycle: {cycle_id} |" in entry:
                cycle_entries.append(entry)
        
        return "\n".join(cycle_entries)
    
def cycle_ids(self) -> List[int]:
    content = self._read_file(self.working_path)
    if not content:
        return []
    
    entries = self._split_entries(content)
    cycles = []
    for entry in entries:
        if not entry.strip():
            continue
        
        # Look for "Cycle:" anywhere in the first few lines
        lines = entry.split('\n')
        for line in lines[:3]:  # Check first 3 lines
            if "Cycle:" in line:
                try:
                    # Extract number after "Cycle:"
                    cycle_str = line.split("Cycle:")[1].strip()
                    # Remove anything after first non-digit
                    cycle_num = ''.join(c for c in cycle_str if c.isdigit())
                    if cycle_num:
                        cycles.append(int(cycle_num))
                        break
                except (ValueError, IndexError):
                    pass
    
    return list(set(cycles))
    
    def _read_file(self, path: Path) -> str:
        """Read a file, returning empty string if it doesn't exist."""
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""
    
    def _write_file(self, path: Path, content: str) -> None:
        """Write content to a file."""
        path.write_text(content.strip() + "\n", encoding="utf-8")
    
    def _split_entries(self, content: str) -> List[str]:
        """Split journal content into individual entries."""
        if not content.strip():
            return []
        
        # Split by "---" separators
        raw_entries = content.split("---\n")
        
        # Clean and filter empty entries
        entries = []
        for entry in raw_entries:
            entry = entry.strip()
            if entry:
                entries.append(entry + "\n\n---")
        
        return entries
    
    def migrate_from_old(self, old_path: Path) -> None:
        """Migrate data from old journal format to new working journal."""
        if not old_path.exists():
            return
        
        content = old_path.read_text(encoding="utf-8")
        if not content.strip():
            return
        
        # Split old entries
        entries = self._split_entries(content)
        
        # Write all to working journal (they'll be limited by working_limit)
        for entry in reversed(entries):  # Reverse so oldest first then newest
            # Try to parse cycle from entry
            lines = entry.split('\n')
            cycle_id = 1
            job = "Migration"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if lines:
                header = lines[0]
                if "Cycle:" in header:
                    try:
                        cycle_str = header.split("Cycle:")[1].split("|")[0].strip()
                        cycle_id = int(cycle_str)
                    except (ValueError, IndexError):
                        pass
                if "Job:" in header:
                    try:
                        job = header.split("Job:")[1].split("|")[0].strip()
                    except IndexError:
                        pass
            
            # Write the entry (this will auto-purge if over limit)
            self.append_reflection(job, entry, cycle_id)
        
        print(f"  → Migrated {len(entries)} entries from {old_path.name} to {self.working_path.name}")