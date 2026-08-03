import time

from backend.cognitive_jobs import (
    ConversationUnderstanding,
    ProjectUnderstanding,
    UserUnderstanding,
    SelfImprovement,
    OpenContemplation,
    Consolidation,
)


class Scheduler:
    def __init__(self):
        self.jobs = [
            ConversationUnderstanding(),
            ProjectUnderstanding(),
            UserUnderstanding(),
            SelfImprovement(),
            OpenContemplation(),
            Consolidation(),
        ]
        self.last_slot = None

    def start(self):
        print("Starting Scheduler...")

        while True:
            slot = int(time.time() // 15) % len(self.jobs)

            if slot != self.last_slot:
                self.last_slot = slot
                self.jobs[slot].run()

            time.sleep(1)