from pydantic import BaseModel
from typing import Dict, Any


class CleanerAction(BaseModel):
    action_type: str
    parameters: Dict[str, Any] = {}
