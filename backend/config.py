# backend/config.py
from pathlib import Path
import yaml
from .workspace import Workspace

def load_workspace(workspace_name):
    """Load workspace configuration by workspace name."""
    config_path = Path(f"config/workspaces/{workspace_name}.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Workspace configuration not found: {config_path}")
    
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
    
    # Create and return a Workspace object
    return Workspace(
        name=workspace_name,
        model=data.get("model", "openai/gpt-oss-120b"),
        system_prompt=data.get("system_prompt", ""),
        workspace=data.get("workspace_dir", f"workspaces/{workspace_name}")
    )