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
            mode: "production" for real time, "test" for compressed timing, "development" for immediate
        """
        self.mode = mode
        
        if mode == "test":
            # Test mode: compressed timing (in seconds)
            self.job_times = [0, 3, 6, 9, 12]  # Seconds within each hour
            self.consolidation_times = [15, 18, 21, 24, 27]  # Seconds within hour 4
            self.hour_duration = 30  # 30 seconds per hour
            self.use_seconds = True
            print("🧪 TEST MODE: Timing compressed (seconds)")
        elif mode == "development":
            # Development mode: run immediately
            self.job_times = [0, 0, 0, 0, 0]
            self.consolidation_times = [0, 0, 0, 0, 0]
            self.hour_duration = 0
            self.use_seconds = True
            print("🛠️ DEVELOPMENT MODE: No waiting")
        else:
            # Production mode: real timing (in minutes)
            self.job_times = [0, 5, 10, 15, 20]  # Minutes within each hour
            self.consolidation_times = [25, 30, 35, 40, 45]  # Minutes within hour 4
            self.hour_duration = 60  # 60 minutes per hour
            self.use_seconds = False
            print("🚀 PRODUCTION MODE: Real timing")
        
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
                "hour": 1,
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

    def wait_until_next_minute(self, target_minute):
        """Wait until the next scheduled time."""
        if self.mode == "development":
            return
        
        now = datetime.now()
        
        if self.use_seconds:
            current = now.second
            max_time = 60
        else:
            current = now.minute
            max_time = 60
        
        if current < target_minute:
            wait = target_minute - current
        else:
            wait = (max_time - current) + target_minute
        
        if wait > 0:
            unit = "seconds" if self.use_seconds else "minutes"
            print(f"  ⏳ Waiting {wait} {unit} until minute {target_minute}")
            
            if self.use_seconds:
                time.sleep(wait)
            else:
                time.sleep(wait * 60)

    def start(self):
        print("🧠 Thinking Partner Scheduler started")
        print(f"  Mode: {self.mode}")
        print(f"  Starting cycle {self.state['cycle_id']}")
        print(f"  Hour: {self.state.get('hour', 1)}")

        while True:
            hour = self.state.get("hour", 1)
            completed_jobs = self.state.get("completed_jobs", [])
            
            # Check if all journals have cycle 4 and we're in hour 4
            all_cycles_4 = all(
                cycle_id in journal.cycle_ids()
                for cycle_id, journal in zip([4]*5, self.journals.values())
            )
            
            if hour == 4 and all_cycles_4 and len(self.state.get("completed_consolidations", [])) < 5:
                self.run_consolidation_phase()
                continue
            
            if hour == 4 and all_cycles_4 and len(self.state.get("completed_consolidations", [])) >= 5:
                # All done, reset
                print("  ✅ Full cycle complete. Resetting to cycle 1")
                self.state["cycle_id"] = 1
                self.state["hour"] = 1
                self.state["completed_jobs"] = []
                self.state["completed_consolidations"] = []
                self.state["cycle_start_time"] = datetime.now().isoformat()
                self.save_state()
                continue
            
            # Regular job scheduling
            status = self.synchronization_status()
            if status["ahead"]:
                print("⚠️ Scheduler stopped: journal is ahead of global cycle.")
                print(status)
                return
            
            # Check which jobs need to run
            for i, job in enumerate(self.jobs):
                job_name = job.__class__.__name__
                
                if job_name in completed_jobs:
                    continue
                
                # Wait until this job's scheduled time
                target_time = self.job_times[i]
                self.wait_until_next_minute(target_time)
                
                # Run the job
                print(f"  → Running {job_name} (cycle {self.state['cycle_id']}, hour {hour}) at {datetime.now().strftime('%H:%M:%S')}")
                job.run(self.state["cycle_id"])
                
                self.state["completed_jobs"].append(job_name)
                self.save_state()
                break  # Only run one job per loop
            
            # Check if all jobs for this hour are complete
            if len(self.state["completed_jobs"]) >= 5:
                if hour == 4:
                    # Hour 4 complete, move to consolidation
                    print("  ✅ Hour 4 complete. Moving to consolidation phase.")
                    self.state["completed_consolidations"] = []
                    self.save_state()
                else:
                    # Move to next hour
                    self.state["hour"] = hour + 1
                    self.state["cycle_id"] = hour + 1
                    self.state["completed_jobs"] = []
                    self.save_state()
                    print(f"  → Moved to hour {self.state['hour']} (cycle {self.state['cycle_id']})")

    def run_consolidation_phase(self):
        """Run consolidations."""
        completed_consolidations = self.state.get("completed_consolidations", [])
        consolidation_index = len(completed_consolidations)
        
        if consolidation_index >= 5:
            return
        
        # Wait until this consolidation's scheduled time
        target_time = self.consolidation_times[consolidation_index]
        self.wait_until_next_minute(target_time)
        
        job_name = self.jobs[consolidation_index].__class__.__name__
        
        print(f"  → Consolidating {job_name} journal...")
        self.consolidation.run()
        print("  ✓ Consolidation complete")
        
        print(f"  → Updating canonical memory for {job_name}...")
        canonical_update = CanonicalUpdateJob()
        canonical_update.run()
        print("  ✓ Canonical update complete")
        
        self.state["completed_consolidations"].append(job_name)
        self.save_state()

def main():
    import sys
    
    mode = "production"
    if len(sys.argv) > 1:
        if sys.argv[1] == "--dev":
            mode = "development"
        elif sys.argv[1] == "--test":
            mode = "test"
    
    scheduler = Scheduler(mode=mode)
    scheduler.start()

if __name__ == "__main__":
    main()