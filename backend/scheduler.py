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
        
        # Job timing (in minutes)
        self.job_times = [0, 5, 10, 15, 20]  # Minutes within each hour
        self.consolidation_times = [25, 30, 35, 40, 45]  # Minutes within hour 4
        
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

        self.state_path = Path("cognitive_state.json")
        self.state = self.load_state()
        self.reconcile_state()
        self.rebuild_completed_jobs()
        self.save_state()

    def load_state(self):
        if not self.state_path.exists():
            return {
                "cycle_id": 1,
                "completed_jobs": [],
                "cycle_start_time": datetime.now().isoformat(),
                "hour": 1,  # Track which hour we're in (1-4)
            }

        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def save_state(self):
        self.state_path.write_text(
            json.dumps(self.state, indent=2),
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

        has_numeric_cycles = any(cycles for cycles in journal_cycles.values())
        
        if not has_numeric_cycles:
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

    def get_next_job_minute(self):
        """Get the next scheduled minute for a job."""
        hour = self.state.get("hour", 1)
        
        # If we're in consolidation phase (hour 4, after minute 20)
        if hour == 4 and len(self.state.get("completed_jobs", [])) >= 5:
            # We're in consolidation phase
            completed_consolidations = len(self.state.get("completed_consolidations", []))
            if completed_consolidations < 5:
                return self.consolidation_times[completed_consolidations]
            else:
                # All consolidations done, move to next cycle
                return None
        
        # Regular job schedule
        completed_jobs = len(self.state.get("completed_jobs", []))
        if completed_jobs < 5:
            return self.job_times[completed_jobs]
        else:
            # All jobs done for this hour
            return None

    def wait_until_next_job(self):
        """Wait until the next scheduled job time."""
        if self.mode == "development":
            return
        
        next_minute = self.get_next_job_minute()
        if next_minute is None:
            # No more jobs this hour
            return
        
        now = datetime.now()
        current_minute = now.minute
        
        # Calculate wait time
        if current_minute < next_minute:
            wait_minutes = next_minute - current_minute
        else:
            # Next hour
            wait_minutes = (60 - current_minute) + next_minute
        
        wait_seconds = wait_minutes * 60
        
        print(f"  ⏳ Waiting {wait_minutes} minutes until next job at minute {next_minute}")
        time.sleep(wait_seconds)

    def start(self):
        print("🧠 Thinking Partner Scheduler started")
        print(f"  Mode: {self.mode}")
        print(f"  Starting cycle {self.state['cycle_id']}")
        print(f"  Hour: {self.state.get('hour', 1)}")
        print(f"  Cycle start time: {self.state['cycle_start_time']}")

        while True:
            # Wait until the next scheduled job time
            self.wait_until_next_job()
            
            hour = self.state.get("hour", 1)
            completed_jobs = len(self.state.get("completed_jobs", []))
            
            # Check if we're in consolidation phase (hour 4, all 5 jobs done)
            if hour == 4 and completed_jobs >= 5:
                self.run_consolidation_phase()
                continue
            
            # Run regular jobs
            status = self.synchronization_status()

            if status["ahead"]:
                print("⚠️ Scheduler stopped: journal is ahead of global cycle.")
                print(status)
                return

            # Find and run the next job
            for i, job in enumerate(self.jobs):
                job_name = job.__class__.__name__
                
                # Check if this job should run at the current minute
                if i < len(self.job_times):
                    current_minute = datetime.now().minute
                    if current_minute != self.job_times[i]:
                        continue
                
                if job_name in self.state["completed_jobs"]:
                    continue

                print(f"  → Running {job_name} (cycle {self.state['cycle_id']}, hour {hour}) at {datetime.now().strftime('%H:%M:%S')}")
                job.run(self.state["cycle_id"])

                self.state["completed_jobs"].append(job_name)
                self.save_state()
                break  # Only run one job per minute
            
            # Check if all jobs for this hour are complete
            if len(self.state["completed_jobs"]) >= 5:
                if hour == 4:
                    # Hour 4 complete, move to consolidation phase
                    print(f"  ✅ Hour 4 complete. Moving to consolidation phase.")
                    self.state["cycle_id"] = 4  # Keep cycle_id at 4 for consolidation
                    self.state["completed_consolidations"] = []
                    self.state["completed_jobs"] = []  # Clear jobs
                    self.save_state()
                else:
                    # Move to next hour
                    self.state["hour"] = hour + 1
                    self.state["cycle_id"] = hour + 1
                    self.state["completed_jobs"] = []
                    self.save_state()
                    print(f"  → Moved to hour {self.state['hour']} (cycle {self.state['cycle_id']})")

    def run_consolidation_phase(self):
        """Run consolidations at minutes 25, 30, 35, 40, 45."""
        completed_consolidations = self.state.get("completed_consolidations", [])
        
        # Determine which consolidation to run next
        if len(completed_consolidations) >= 5:
            # All consolidations done, reset everything
            print(f"  ✅ All consolidations complete. Resetting for next cycle.")
            self.state["cycle_id"] = 1
            self.state["hour"] = 1
            self.state["completed_jobs"] = []
            self.state["completed_consolidations"] = []
            self.state["cycle_start_time"] = datetime.now().isoformat()
            self.save_state()
            print(f"  ✓ Full cycle complete. Resetting to cycle 1")
            return
        
        # Run the next consolidation
        consolidation_index = len(completed_consolidations)
        job_name = self.jobs[consolidation_index].__class__.__name__
        
        print(f"  → Consolidating {job_name} journal...")
        self.consolidation.run()
        print(f"  ✓ Consolidation complete")
        
        print(f"  → Updating canonical memory for {job_name}...")
        canonical_update = CanonicalUpdateJob()
        canonical_update.run()
        print(f"  ✓ Canonical update complete")
        
        self.state["completed_consolidations"].append(job_name)
        self.save_state()

def main():
    import sys
    
    mode = "production"
    if len(sys.argv) > 1 and sys.argv[1] == "--dev":
        mode = "development"
    
    scheduler = Scheduler(mode=mode)
    scheduler.start()

if __name__ == "__main__":
    main()