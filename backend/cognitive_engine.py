from backend.scheduler import Scheduler


class CognitiveEngine:
    def __init__(self):
        self.scheduler = Scheduler()

    def start(self):
        print("Starting Cognitive Engine...")
        self.scheduler.start()


if __name__ == "__main__":
    engine = CognitiveEngine()

    try:
        engine.start()
    except KeyboardInterrupt:
        print("\nStopping Cognitive Engine...")