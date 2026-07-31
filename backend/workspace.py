from dataclasses import dataclass


@dataclass
class Workspace:
    name: str
    model: str
    system_prompt: str
    workspace: str