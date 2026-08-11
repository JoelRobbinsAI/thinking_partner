from pathlib import Path
import hashlib
from backend.journal_embeddings import JournalEmbeddings

class CanonicalEmbeddings:
    def __init__(self, workspace_name="clinical"):
        self.workspace_name = workspace_name
        self.canonical_dir = Path(f"workspaces/{workspace_name}/canonical")
        self.journal_embeddings = JournalEmbeddings(workspace_name=workspace_name)
        self.collection = self.journal_embeddings.collection  # Share the same collection
    
    def embed_all(self):
        """Embed all canonical memory sections."""
        if not self.canonical_dir.exists():
            print(f"⚠️ No canonical directory for {self.workspace_name}")
            return
        
        for filepath in self.canonical_dir.glob("*.md"):
            self._embed_file(filepath)
    
    def _embed_file(self, filepath):
        """Embed a single canonical file by sections."""
        content = filepath.read_text(encoding="utf-8")
        
        # Split by ## headings (sections)
        sections = self._split_sections(content)
        
        for section_name, section_text in sections:
            # Create a unique ID
            entry_id = hashlib.md5(
                f"canonical_{filepath.stem}_{section_name}_{section_text[:100]}".encode()
            ).hexdigest()
            
            # Check if already exists
            try:
                existing = self.collection.get(ids=[entry_id])
                if existing and existing['ids']:
                    continue  # Skip if already embedded
            except:
                pass
            
            # Add to collection
            self.collection.add(
                documents=[section_text],
                metadatas=[{
                    "type": "canonical",
                    "file": filepath.stem,
                    "section": section_name,
                    "workspace": self.workspace_name
                }],
                ids=[entry_id]
            )
        
        print(f"✅ Embedded canonical sections from {filepath.name}")
    
    def _split_sections(self, content):
        """Split markdown content into sections by ## headings."""
        sections = []
        lines = content.splitlines()
        
        current_section = "overview"
        current_text = []
        
        for line in lines:
            if line.startswith("## "):
                if current_text:
                    sections.append((current_section, "\n".join(current_text).strip()))
                current_section = line[3:].strip()
                current_text = []
            else:
                current_text.append(line)
        
        if current_text:
            sections.append((current_section, "\n".join(current_text).strip()))
        
        return sections