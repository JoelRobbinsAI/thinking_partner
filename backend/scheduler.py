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

    def start(self):
        print("Starting Scheduler...")

        for job in self.jobs:
            job.run()