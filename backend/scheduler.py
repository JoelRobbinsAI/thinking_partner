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
            self.use_seconds = True
            print("🧪 TEST MODE: Timing compressed (seconds)")
        elif mode == "development":
            # Development mode: run immediately
            self.job_times = [0, 0, 0, 0, 0]
            self.consolidation_times = [0, 0, 0, 0, 0]
            self.use_seconds = True
            print("🛠️ DEVELOPMENT MODE: No waiting")
        else:
            # Production mode: real timing (in minutes)
            self.job_times = [0, 5, 10, 15, 20]  # Minutes within each hour
            self.consolidation_times = [25, 30, 35, 40, 45]  # Minutes within hour 4
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
                "conversation"
            ),
            "ProjectUnderstanding": CognitiveJournal(
                "projects"
            ),
            "UserUnderstanding": CognitiveJournal(
                "user"
            ),
            "SelfImprovement": CognitiveJournal(
                "self"
            ),
            "OpenContemplation": CognitiveJournal(
                "open_contemplation"
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
                "completed_consolidations": [],
                "cycle_start_time": datetime.now().isoformat(),
                "hour": 1,
                "phase": "jobs",  # "jobs" or "consolidation"
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
            self.state["completed_consolidations"] = []

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
        print(f"  Phase: {self.state.get('phase', 'jobs')}")

        while True:
            hour = self.state.get("hour", 1)
            phase = self.state.get("phase", "jobs")
            
            # Check if we should be in consolidation phase (only in hour 4)
            if hour == 4 and phase == "jobs":
                # Check if all jobs for this hour are complete
                completed_jobs = self.state.get("completed_jobs", [])
                # Check if ALL 5 jobs are complete
                all_jobs_complete = all(
                    job.__class__.__name__ in completed_jobs
                    for job in self.jobs
                )
                if all_jobs_complete:
                    print("  ✅ All jobs complete for hour 4. Moving to consolidation phase.")
                    self.state["phase"] = "consolidation"
                    self.state["completed_consolidations"] = []
                    self.save_state()
                    phase = "consolidation"
            
            # Handle consolidation phase (still in hour 4)
            if phase == "consolidation":
                completed_consolidations = self.state.get("completed_consolidations", [])
                
                # Check if all consolidations are done
                if len(completed_consolidations) >= 5:
                    # All done, reset to cycle 1, hour 1
                    print("  ✅ All consolidations complete. Resetting to cycle 1, hour 1")
                    self.state["cycle_id"] = 1
                    self.state["hour"] = 1
                    self.state["phase"] = "jobs"
                    self.state["completed_jobs"] = []
                    self.state["completed_consolidations"] = []
                    self.state["cycle_start_time"] = datetime.now().isoformat()
                    self.save_state()
                    continue
                
                # Run the next consolidation
                consolidation_index = len(completed_consolidations)
                
                # Wait until this consolidation's scheduled time
                target_time = self.consolidation_times[consolidation_index]
                self.wait_until_next_minute(target_time)
                
                job_name = self.jobs[consolidation_index].__class__.__name__
                
                print(f"  → Consolidating {job_name} journal (cycle {self.state['cycle_id']}, hour 4)...")
                self.consolidation.run(self.state["cycle_id"])
                print("  ✓ Consolidation complete")
                
                print(f"  → Updating canonical memory for {job_name}...")
                canonical_update = CanonicalUpdateJob()
                canonical_update.run()
                print("  ✓ Canonical update complete")
                
                self.state["completed_consolidations"].append(job_name)
                self.save_state()
                continue
            
            # Regular job scheduling (hours 1-4)
            completed_jobs = self.state.get("completed_jobs", [])
            
            # 🔍 RECOVERY: Check if any journal is missing the current cycle
            missing_jobs = []
            for job in self.jobs:
                job_name = job.__class__.__name__
                journal = self.journals[job_name]
                if self.state["cycle_id"] not in journal.cycle_ids():
                    missing_jobs.append(job_name)
            
            if missing_jobs:
                print(f"  ⚠️ Missing cycle {self.state['cycle_id']} in journals: {missing_jobs}")
                # Remove missing jobs from completed_jobs so they'll run
                for missing in missing_jobs:
                    if missing in completed_jobs:
                        completed_jobs.remove(missing)
                        print(f"  🔄 Removed {missing} from completed_jobs (will retry)")
                        self.state["completed_jobs"] = completed_jobs
                        self.save_state()
            
            # Check if all jobs for this hour are complete
            all_jobs_complete = all(
                job.__class__.__name__ in self.state["completed_jobs"]
                for job in self.jobs
            )
            
            if all_jobs_complete:
                if hour < 4:
                    # Move to next hour - increment both hour AND cycle_id
                    self.state["hour"] = hour + 1
                    self.state["cycle_id"] = hour + 1
                    self.state["completed_jobs"] = []
                    self.save_state()
                    print(f"  → Moved to hour {self.state['hour']} (cycle {self.state['cycle_id']})")
                    continue
                else:
                    # Hour 4 complete - will move to consolidation in next loop
                    continue
            
            # Run jobs for this hour
            status = self.synchronization_status()
            if status["ahead"]:
                print("⚠️ Scheduler stopped: journal is ahead of global cycle.")
                print(status)
                return
            
            # Find the next job to run
            for i, job in enumerate(self.jobs):
                job_name = job.__class__.__name__
                
                if job_name in self.state["completed_jobs"]:
                    continue
                
                # Wait until this job's scheduled time
                target_time = self.job_times[i]
                self.wait_until_next_minute(target_time)
                
                # Run the job
                print(f"  → Running {job_name} (cycle {self.state['cycle_id']}, hour {hour}) at {datetime.now().strftime('%H:%M:%S')}")
                job.run(self.state["cycle_id"])
                
                # Verify the journal was actually written
                journal = self.journals[job_name]
                if self.state["cycle_id"] in journal.cycle_ids():
                    print(f"  ✅ Journal {job_name} confirmed with cycle {self.state['cycle_id']}")
                else:
                    print(f"  ❌ ERROR: Journal {job_name} was NOT written! Will retry next loop.")
                    # Don't mark as complete - it will retry
                    continue
                
                self.state["completed_jobs"].append(job_name)
                self.save_state()
                break  # Only run one job per loop iteration

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