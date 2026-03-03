# filename: modern_app/app/service.py
from __future__ import annotations

from typing import Any, Dict, Optional, List
import uuid

from .repo import IssueRepository
from .timeutil import utc_now_z
from .cache import LRUCache

class IssueService:
    def __init__(self, repo: IssueRepository, cache_capacity: int = 256):
        self.repo = repo
        self.cache = LRUCache[str, Dict[str, Any]](capacity=cache_capacity)


    def list_issues(self, status: Optional[str], priority: Optional[str]) -> List[Dict[str, Any]]:
        issues = self.repo.list_issues()

        # Preserve legacy behavior: naive string filtering
        if status is not None:
            issues = [i for i in issues if i.get("status") == status]
        if priority is not None:
            issues = [i for i in issues if i.get("priority") == priority]

        return issues

    def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        cached = self.cache.get(issue_id)
        if cached is not None:
            return cached

        issue = self.repo.get_issue_by_id(issue_id)
        if issue is not None:
            self.cache.set(issue_id, issue)
        return issue

    def create_issue(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = utc_now_z()
        issue = dict(payload)
        issue["id"] = str(uuid.uuid4())
        issue["created_at"] = now
        issue["updated_at"] = now

        saved = self.repo.insert_issue(issue)
        self.cache.set(saved["id"], saved)   # keep cache warm
        return saved

    def update_issue(self, issue_id: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        existing = self.repo.get_issue_by_id(issue_id)
        if existing is None:
            return None

        updated = dict(payload)
        updated["id"] = issue_id
        updated["created_at"] = existing.get("created_at")
        updated["updated_at"] = utc_now_z()

        saved = self.repo.update_issue(issue_id, updated)
        if saved is not None:
            self.cache.set(issue_id, saved)  # refresh cache
        return saved
