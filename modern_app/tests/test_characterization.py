# filename: modern_app/tests/test_characterization.py
from fastapi.testclient import TestClient
from modern_app.app.main import app
#from legacy_app.app import app

client = TestClient(app)

def test_create_issue_returns_required_fields():
    response = client.post(
        "/issues",
        json={
            "title": "Test issue",
            "description": "Testing",
            "priority": "high",
            "status": "open",
            "assignee": "rob"
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["title"] == "Test issue"
    assert data["priority"] == "high"
    assert "created_at" in data
    assert "updated_at" in data


def test_issue_persists_after_creation():
    create = client.post(
        "/issues",
        json={
            "title": "Persist Test",
            "description": "Testing",
            "priority": "low",
            "status": "open",
            "assignee": None
        },
    )

    issue_id = create.json()["id"]

    get_response = client.get(f"/issues/{issue_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == issue_id


def test_filter_by_priority():
    client.post(
        "/issues",
        json={
            "title": "High priority",
            "description": "Testing",
            "priority": "high",
            "status": "open",
            "assignee": None
        },
    )

    response = client.get("/issues?priority=high")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_repeated_get_returns_same_issue():
    create = client.post(
        "/issues",
        json={
            "title": "Cache test",
            "description": "Testing",
            "priority": "medium",
            "status": "open",
            "assignee": None
        },
    )
    issue_id = create.json()["id"]

    first = client.get(f"/issues/{issue_id}").json()
    second = client.get(f"/issues/{issue_id}").json()

    assert first["id"] == second["id"]
    assert first["title"] == second["title"]
