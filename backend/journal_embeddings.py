import chromadb
from pathlib import Path
from datetime import datetime
import hashlib
import re

class JournalEmbeddings:
    def __init__(self, workspace_name="clinical", persist_dir="./chroma_db"):
        self.workspace_name = workspace_name
        self.journal_path = Path(f"workspaces/{workspace_name}/cognitive_journals")
        """Initialize ChromaDB for journal embeddings."""
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=f"journals_{workspace_name}",
            metadata={"hnsw:space": "cosine"}
        )
        # Journal name mapping
        self.journal_map = {
            "ConversationUnderstanding": "conversation.md",
            "ProjectUnderstanding": "projects.md",
            "UserUnderstanding": "user.md",
            "SelfImprovement": "self.md",
            "OpenContemplation": "open_contemplation.md"
        }
        
    def _get_journal_entries(self, journal_name):
        """Read all entries from a specific journal."""
        filename = self.journal_map.get(journal_name)
        if not filename:
            return []
        
        filepath = self.journal_path / filename
        if not filepath.exists():
            return []
        
        content = filepath.read_text(encoding="utf-8")
        
        # Parse entries with cycle_id markers
        entries = []
        # Find all entries that start with "### Cycle"
        pattern = r"### Cycle (\d+).*?\n(.*?)(?=\n### Cycle|\Z)"
        matches = re.findall(pattern, content, re.DOTALL)
        
        for cycle_id, entry_text in matches:
            entries.append({
                "cycle_id": int(cycle_id),
                "text": entry_text.strip(),
                "journal_name": journal_name
            })
        
        return entries
    
    def get_all_entries(self):
        """Get all journal entries from all journals."""
        all_entries = []
        for journal_name in self.journal_map.keys():
            entries = self._get_journal_entries(journal_name)
            for entry in entries:
                entry["journal_name"] = journal_name
                all_entries.append(entry)
        return all_entries
    
    def get_existing_ids(self):
        """Get all existing document IDs in the collection."""
        # Chroma doesn't have a direct way to get all IDs
        # We'll store them in a separate file
        id_file = Path("chroma_db/ids.txt")
        if id_file.exists():
            return set(id_file.read_text(encoding="utf-8").splitlines())
        return set()
    
    def save_ids(self, ids):
        """Save IDs to a file."""
        id_file = Path("chroma_db/ids.txt")
        id_file.parent.mkdir(parents=True, exist_ok=True)
        id_file.write_text("\n".join(ids), encoding="utf-8")
    
    def embed_all(self, force=False):
        """Embed all journal entries."""
        entries = self.get_all_entries()
        existing_ids = self.get_existing_ids() if not force else set()
        
        new_entries = []
        new_ids = []
        
        for entry in entries:
            # Create a unique ID
            entry_id = hashlib.md5(
                f"{entry['journal_name']}{entry['cycle_id']}{entry['text'][:100]}".encode()
            ).hexdigest()
            
            if entry_id not in existing_ids:
                new_entries.append(entry)
                new_ids.append(entry_id)
        
        if not new_entries:
            print("✅ No new journal entries to embed")
            return
        
        print(f"📝 Embedding {len(new_entries)} new journal entries...")
        
        # Add to Chroma in batches
        for i, entry in enumerate(new_entries):
            self.collection.add(
                documents=[entry["text"]],
                metadatas=[{
                    "journal_name": entry["journal_name"],
                    "cycle_id": entry["cycle_id"],
                    "timestamp": datetime.now().isoformat()
                }],
                ids=[new_ids[i]]
            )
        
        # Update IDs file
        all_ids = existing_ids.union(set(new_ids))
        self.save_ids(list(all_ids))
        
        print(f"✅ Embedded {len(new_entries)} entries")
    
    def search(self, query_text, journal_type=None, n_results=5):
        """Search for relevant journal entries."""
        where_filter = {"journal_name": journal_type} if journal_type else None
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_filter
        )
        
        # Format results
        formatted_results = []
        if results and results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "text": results['documents'][0][i],
                    "journal_name": results['metadatas'][0][i]['journal_name'],
                    "cycle_id": results['metadatas'][0][i]['cycle_id'],
                    "distance": results['distances'][0][i] if results.get('distances') else None
                })
        
        return formatted_results
    
    def search_all_journals(self, query_text, n_results=5):
        """Search across all journals."""
        return self.search(query_text, journal_type=None, n_results=n_results)
    
    def search_by_journal(self, query_text, journal_name, n_results=3):
        """Search within a specific journal."""
        return self.search(query_text, journal_type=journal_name, n_results=n_results)