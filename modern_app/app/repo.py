# filename: modern_app/app/repo.py
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "legacy_app", "db.json")

class IssueRepository:
    def load_db(self) -> Dict[str, Any]:
        if not os.path.exists(DB_FILE):
            return {"issues": []}
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_db(self, db: Dict[str, Any]) -> None:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2)

    def list_issues(self) -> List[Dict[str, Any]]:
        db = self.load_db()
        return db.get("issues", [])

    def get_issue_by_id(self, issue_id: str) -> Optional[Dict[str, Any]]:
        for issue in self.list_issues():
            if issue.get("id") == issue_id:
                return issue
        return None

    def insert_issue(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        db = self.load_db()
        db.setdefault("issues", []).append(issue)
        self.save_db(db)
        return issue

    def update_issue(self, issue_id: str, updated_issue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        db = self.load_db()
        issues = db.get("issues", [])
        for idx, issue in enumerate(issues):
            if issue.get("id") == issue_id:
                issues[idx] = updated_issue
                self.save_db(db)
                return updated_issue
        return None
