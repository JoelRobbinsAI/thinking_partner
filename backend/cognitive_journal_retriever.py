from backend.cognitive_journal import CognitiveJournal


class CognitiveJournalRetriever:
    def __init__(self, filename, recent_entries=2):
        self.journal = CognitiveJournal(filename)
        self.recent_entries = recent_entries

    def retrieve(self):
        return self.journal.read_recent(
            self.recent_entries
        )