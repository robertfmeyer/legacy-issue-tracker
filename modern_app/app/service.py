# filename: modern_app/app/service.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
import uuid

from .repo import IssueRepository
from .timeutil import utc_now_z

class IssueService:
    def __init__(self, repo: IssueRepository):
        self.repo = repo

    def list_issues(self, status: Optional[str], priority: Optional[str]) -> List[Dict[str, Any]]:
        issues = self.repo.list_issues()

        # Preserve legacy behavior: naive string filtering
        if status is not None:
            issues = [i for i in issues if i.get("status") == status]
        if priority is not None:
            issues = [i for i in issues if i.get("priority") == priority]

        return issues

    def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_issue_by_id(issue_id)

    def create_issue(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = utc_now_z()
        issue = dict(payload)
        issue["id"] = str(uuid.uuid4())
        issue["created_at"] = now
        issue["updated_at"] = now
        return self.repo.insert_issue(issue)

    def update_issue(self, issue_id: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        existing = self.repo.get_issue_by_id(issue_id)
        if existing is None:
            return None

        updated = dict(payload)
        updated["id"] = issue_id
        updated["created_at"] = existing.get("created_at")
        updated["updated_at"] = utc_now_z()
        return self.repo.update_issue(issue_id, updated)
