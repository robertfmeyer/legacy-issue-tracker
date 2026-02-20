# filename: legacy_app/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import os
import uuid
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "db.json")

app = FastAPI(title="Legacy Issue Tracker (Intentionally Legacy)")

class IssueIn(BaseModel):
    title: str
    description: str
    priority: str = "medium"   # "low" | "medium" | "high"
    status: str = "open"       # "open" | "in_progress" | "closed"
    assignee: Optional[str] = None

def _load_db() -> Dict[str, Any]:
    if not os.path.exists(DB_FILE):
        return {"issues": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_db(db: Dict[str, Any]) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

@app.get("/issues")
def list_issues(status: Optional[str] = None, priority: Optional[str] = None) -> List[Dict[str, Any]]:
    db = _load_db()
    issues = db.get("issues", [])

    # Intentionally naive filtering + stringly-typed fields
    if status is not None:
        issues = [i for i in issues if i.get("status") == status]
    if priority is not None:
        issues = [i for i in issues if i.get("priority") == priority]

    return issues

@app.get("/issues/{issue_id}")
def get_issue(issue_id: str) -> Dict[str, Any]:
    db = _load_db()
    for issue in db.get("issues", []):
        if issue.get("id") == issue_id:
            return issue
    raise HTTPException(status_code=404, detail="Issue not found")

@app.post("/issues")
def create_issue(payload: IssueIn) -> Dict[str, Any]:
    db = _load_db()

    issue = payload.model_dump()
    issue["id"] = str(uuid.uuid4())
    issue["created_at"] = datetime.utcnow().isoformat() + "Z"
    issue["updated_at"] = issue["created_at"]

    db.setdefault("issues", []).append(issue)
    _save_db(db)
    return issue

@app.put("/issues/{issue_id}")
def update_issue(issue_id: str, payload: IssueIn) -> Dict[str, Any]:
    db = _load_db()
    issues = db.get("issues", [])

    for idx, issue in enumerate(issues):
        if issue.get("id") == issue_id:
            updated = payload.model_dump()
            updated["id"] = issue_id
            updated["created_at"] = issue.get("created_at")
            updated["updated_at"] = datetime.utcnow().isoformat() + "Z"
            issues[idx] = updated
            _save_db(db)
            return updated

    raise HTTPException(status_code=404, detail="Issue not found")
