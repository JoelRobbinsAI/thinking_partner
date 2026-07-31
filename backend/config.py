import yaml

from .workspace import Workspace


def load_workspace(config_path):
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)

    return Workspace(**data)