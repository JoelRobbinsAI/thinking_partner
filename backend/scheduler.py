import json
from pathlib import Path

from backend.canonical_update_job import CanonicalUpdateJob

from backend.cognitive_jobs import (
    ConversationUnderstanding,
    ProjectUnderstanding,
    UserUnderstanding,
    SelfImprovement,
    OpenContemplation,
    Consolidation,
)

from backend.cognitive_journal import CognitiveJournal

print("✅ Scheduler imports loaded")

class Scheduler:
    def __init__(self):
        self.jobs = [
            ConversationUnderstanding(),
            ProjectUnderstanding(),
            UserUnderstanding(),
            SelfImprovement(),
            OpenContemplation(),
        ]

        self.consolidation = Consolidation()

        self.journals = {
            "ConversationUnderstanding": CognitiveJournal(
                "conversation.md"
            ),
            "ProjectUnderstanding": CognitiveJournal(
                "projects.md"
            ),
            "UserUnderstanding": CognitiveJournal(
                "user.md"
            ),
            "SelfImprovement": CognitiveJournal(
                "self.md"
            ),
            "OpenContemplation": CognitiveJournal(
                "open_contemplation.md"
            ),
        }

        self.state_path = Path(
            "cognitive_state.json"
        )

        self.state = self.load_state()

        self.reconcile_state()

        self.rebuild_completed_jobs()

        self.save_state()

    def load_state(self):
        if not self.state_path.exists():
            return {
                "cycle_id": 1,
                "completed_jobs": [],
            }

        return json.loads(
            self.state_path.read_text(
                encoding="utf-8"
            )
        )

    def save_state(self):
        self.state_path.write_text(
            json.dumps(
                self.state,
                indent=2,
            ),
            encoding="utf-8",
        )

    def reconcile_state(self):
        journal_cycles = [
            journal.cycle_ids()
            for journal in self.journals.values()
        ]

        if not all(journal_cycles):
            return

        latest_cycles = [
            max(cycles)
            for cycles in journal_cycles
        ]

        if len(set(latest_cycles)) != 1:
            return

        latest_cycle = latest_cycles[0]

        if latest_cycle > self.state["cycle_id"]:
            self.state["cycle_id"] = latest_cycle
            self.state["completed_jobs"] = []

    def rebuild_completed_jobs(self):
        cycle_id = self.state["cycle_id"]

        completed_jobs = []

        for job_name, journal in self.journals.items():
            if cycle_id in journal.cycle_ids():
                completed_jobs.append(job_name)

        self.state["completed_jobs"] = completed_jobs

    def synchronization_status(self):
        journal_cycles = {
            name: journal.cycle_ids()
            for name, journal in self.journals.items()
        }

        # Check if any journal has no numeric cycles (only Consolidation entries)
        has_numeric_cycles = any(cycles for cycles in journal_cycles.values())
        
        if not has_numeric_cycles:
            # All journals only have Consolidation entries, so we're at cycle 1
            return {
                "ready": True,
                "cycle_id": 1,
                "journal_cycles": journal_cycles,
                "ahead": [],
                "behind": [],
            }

        if not all(journal_cycles.values()):
            return {
                "ready": False,
                "cycle_id": self.state["cycle_id"],
                "journal_cycles": journal_cycles,
                "ahead": [],
                "behind": [],
            }

        latest_cycles = {
            name: max(cycles)
            for name, cycles in journal_cycles.items()
        }

        target_cycle = self.state["cycle_id"]

        ahead = [
            name
            for name, cycle_id in latest_cycles.items()
            if cycle_id > target_cycle
            and target_cycle not in journal_cycles[name]
        ]

        behind = [
            name
            for name, cycle_id in latest_cycles.items()
            if cycle_id < target_cycle
        ]

        ready = all(
            job.__class__.__name__ in self.state["completed_jobs"]
            for job in self.jobs
        )

        return {
            "ready": ready,
            "cycle_id": target_cycle,
            "journal_cycles": journal_cycles,
            "ahead": ahead,
            "behind": behind,
        }

    def check_synchronization(self):
        status = self.synchronization_status()

        return status["ready"]

    def start(self):
        print("🧠 Thinking Partner Scheduler started")
        print(f"Starting cycle {self.state['cycle_id']}")

        while True:
            status = self.synchronization_status()

            if status["ahead"]:
                print("⚠️ Scheduler stopped: journal is ahead of global cycle.")
                print(status)
                return

            for job in self.jobs:
                job_name = job.__class__.__name__

                if job_name in self.state["completed_jobs"]:
                    continue

                print(f"  → Running {job_name} (cycle {self.state['cycle_id']})")
                job.run(self.state["cycle_id"])

                self.state["completed_jobs"].append(job_name)
                self.save_state()

            # Move to next cycle or consolidate
            if self.state["cycle_id"] == 4:
                print(f"  → Consolidating cycle 4...")
                self.consolidation.run()
                print(f"  ✓ Consolidation complete")
                
                # Add canonical memory update
                print(f"  → Updating canonical memory...")
                canonical_update = CanonicalUpdateJob()
                canonical_update.run()
                
                self.state["cycle_id"] = 1
                print(f"  → Reset cycle_id to 1")
            else:
                self.state["cycle_id"] += 1
                print(f"  → Incremented cycle_id to {self.state['cycle_id']}")

            self.state["completed_jobs"] = []
            self.save_state()
            
            print(f"  ✓ Cycle complete, next cycle will be {self.state['cycle_id']}")