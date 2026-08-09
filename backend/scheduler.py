import json
import time
from pathlib import Path
from datetime import datetime, timedelta

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
    def __init__(self, mode="production"):
        """
        Initialize scheduler.
        
        Args:
            mode: "production" for time-based scheduling, "development" for immediate execution
        """
        self.mode = mode
        
        # Production timing (in minutes)
        self.job_interval_minutes = 5
        self.consolidation_delay_minutes = 30  # 30 minutes after cycle 4
        self.cycle_duration_hours = 4  # 4 hours to complete 4 cycles
        
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
        
        # Track when the current cycle started
        if "cycle_start_time" not in self.state:
            self.state["cycle_start_time"] = datetime.now().isoformat()
            self.save_state()

    def load_state(self):
        if not self.state_path.exists():
            return {
                "cycle_id": 1,
                "completed_jobs": [],
                "cycle_start_time": datetime.now().isoformat(),
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

    def get_next_job_time(self):
        """Calculate when the next job should run based on the schedule."""
        cycle_start = datetime.fromisoformat(self.state["cycle_start_time"])
        cycle_id = self.state["cycle_id"]
        completed_jobs = len(self.state["completed_jobs"])
        
        # Calculate time offset for this job
        # Job index: 0=Conversation, 1=Project, 2=User, 3=Self, 4=Open
        job_offset_minutes = completed_jobs * self.job_interval_minutes
        
        # Calculate when this job should run
        # Each cycle starts at the beginning of the hour
        # Cycle 1: hour 0, Cycle 2: hour 1, Cycle 3: hour 2, Cycle 4: hour 3
        cycle_hour_offset = (cycle_id - 1) * 1  # 1 hour per cycle
        
        # Base time: cycle_start + cycle_hour_offset hours + job_offset_minutes
        next_time = cycle_start + timedelta(hours=cycle_hour_offset, minutes=job_offset_minutes)
        
        return next_time

    def wait_until_next_job(self):
        """Wait until the next scheduled job time."""
        if self.mode == "development":
            # In development mode, run immediately
            return
        
        next_time = self.get_next_job_time()
        now = datetime.now()
        
        if next_time <= now:
            # If we're past the scheduled time, run immediately
            return
        
        wait_seconds = (next_time - now).total_seconds()
        print(f"  ⏳ Waiting {wait_seconds/60:.1f} minutes until next job at {next_time.strftime('%H:%M:%S')}")
        time.sleep(wait_seconds)

    def start(self):
        print("🧠 Thinking Partner Scheduler started")
        print(f"  Mode: {self.mode}")
        print(f"  Starting cycle {self.state['cycle_id']}")
        print(f"  Cycle start time: {self.state['cycle_start_time']}")
        
        if self.mode == "production":
            print(f"  Job interval: {self.job_interval_minutes} minutes")
            print(f"  Cycle duration: {self.cycle_duration_hours} hours")

        while True:
            # Wait until the next scheduled job time
            self.wait_until_next_job()
            
            # Check if we're in consolidation phase (cycle 4 completed)
            if self.state["cycle_id"] > 4:
                # Handle consolidation
                self.run_consolidation_phase()
                continue
            
            # Run regular jobs
            status = self.synchronization_status()

            if status["ahead"]:
                print("⚠️ Scheduler stopped: journal is ahead of global cycle.")
                print(status)
                return

            # Run jobs that haven't been completed
            jobs_ran = 0
            for job in self.jobs:
                job_name = job.__class__.__name__

                if job_name in self.state["completed_jobs"]:
                    continue

                print(f"  → Running {job_name} (cycle {self.state['cycle_id']}) at {datetime.now().strftime('%H:%M:%S')}")
                job.run(self.state["cycle_id"])

                self.state["completed_jobs"].append(job_name)
                self.save_state()
                jobs_ran += 1
            
            # Check if all jobs for this cycle are complete
            if len(self.state["completed_jobs"]) >= len(self.jobs):
                # Move to next cycle
                if self.state["cycle_id"] == 4:
                    # Cycle 4 complete, move to consolidation phase
                    print(f"  ✅ Cycle 4 complete. Moving to consolidation phase.")
                    self.state["cycle_id"] = 5  # Use 5 to indicate consolidation phase
                    self.state["completed_jobs"] = []
                    
                    # Record when consolidation should start (30 minutes after cycle 4 completes)
                    consolidation_start = datetime.now() + timedelta(minutes=self.consolidation_delay_minutes)
                    self.state["consolidation_start_time"] = consolidation_start.isoformat()
                    print(f"  ⏳ Consolidation will start at {consolidation_start.strftime('%H:%M:%S')} ({self.consolidation_delay_minutes} minutes)")
                    self.save_state()
                else:
                    self.state["cycle_id"] += 1
                    print(f"  → Incremented cycle_id to {self.state['cycle_id']}")
                    self.state["completed_jobs"] = []
                    self.save_state()
            
            print(f"  ✓ Cycle {self.state['cycle_id']} in progress")

    def run_consolidation_phase(self):
        """Run consolidation and canonical updates."""
        # Check if it's time for consolidation
        if "consolidation_start_time" in self.state:
            consolidation_start = datetime.fromisoformat(self.state["consolidation_start_time"])
            now = datetime.now()
            
            if now < consolidation_start:
                # Wait until consolidation time
                wait_seconds = (consolidation_start - now).total_seconds()
                if wait_seconds > 0:
                    print(f"  ⏳ Waiting {wait_seconds/60:.1f} minutes until consolidation at {consolidation_start.strftime('%H:%M:%S')}")
                    time.sleep(wait_seconds)
        
        # Run consolidation
        print(f"  → Consolidating cycle 4...")
        self.consolidation.run()
        print(f"  ✓ Consolidation complete")
        
        # Run canonical update
        print(f"  → Updating canonical memory...")
        canonical_update = CanonicalUpdateJob()
        canonical_update.run()
        print(f"  ✓ Canonical update complete")
        
        # Reset for next cycle
        self.state["cycle_id"] = 1
        self.state["completed_jobs"] = []
        self.state["cycle_start_time"] = datetime.now().isoformat()
        if "consolidation_start_time" in self.state:
            del self.state["consolidation_start_time"]
        self.save_state()
        
        print(f"  ✓ Full cycle complete. Resetting to cycle 1")
        print(f"  Next cycle starts at {self.state['cycle_start_time']}")

def main():
    import sys
    
    # Check for mode argument
    mode = "production"
    if len(sys.argv) > 1 and sys.argv[1] == "--dev":
        mode = "development"
    
    scheduler = Scheduler(mode=mode)
    scheduler.start()

if __name__ == "__main__":
    main()