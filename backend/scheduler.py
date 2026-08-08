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
        ]

        self.consolidation = Consolidation()
        self.cycle = 0

    def start(self):
        print("Starting Scheduler...")

        while True:
            for job in self.jobs:
                job.run()

            self.cycle += 1

            if self.cycle % 4 == 0:
                self.consolidation.run()