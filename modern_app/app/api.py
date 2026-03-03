# filename: modern_app/app/api.py
from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any, List

from .models import IssueIn
from .repo import IssueRepository
from .service import IssueService

router = APIRouter()

_repo = IssueRepository()
_service = IssueService(_repo)

@router.get("/issues")
def list_issues(status: Optional[str] = None, priority: Optional[str] = None) -> List[Dict[str, Any]]:
    return _service.list_issues(status=status, priority=priority)

@router.get("/issues/{issue_id}")
def get_issue(issue_id: str) -> Dict[str, Any]:
    issue = _service.get_issue(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@router.post("/issues")
def create_issue(payload: IssueIn) -> Dict[str, Any]:
    return _service.create_issue(payload.model_dump())

@router.put("/issues/{issue_id}")
def update_issue(issue_id: str, payload: IssueIn) -> Dict[str, Any]:
    updated = _service.update_issue(issue_id, payload.model_dump())
    if updated is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return updated
