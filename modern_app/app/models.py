# filename: modern_app/app/models.py
from pydantic import BaseModel
from typing import Optional

class IssueIn(BaseModel):
    title: str
    description: str
    priority: str = "medium"
    status: str = "open"
    assignee: Optional[str] = None
