from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from marco.api.approvals import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def approval_payload() -> dict:
    return {
        "task_id": str(uuid4()),
        "tool_request_id": str(uuid4()),
        "tool": "browser",
        "action": "send",
        "risk": "high",
        "reason": "sensitive_action",
        "requires_human_approval": True,
        "target": "example.com",
    }


def test_create_and_get_approval():
    response = client.post("/approvals", json=approval_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"

    approval_id = data["id"]
    response = client.get(f"/approvals/{approval_id}")

    assert response.status_code == 200
    assert response.json()["id"] == approval_id


def test_approve_request():
    response = client.post("/approvals", json=approval_payload())
    approval_id = response.json()["id"]

    response = client.post(
        f"/approvals/{approval_id}/decision",
        json={
            "approved": True,
            "decided_by": "human",
            "comment": "Approved for execution.",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["approval_id"] == approval_id
    assert body["approved"] is True
    assert body["decided_by"] == "human"
    assert body["comment"] == "Approved for execution."


def test_deny_request():
    response = client.post("/approvals", json=approval_payload())
    approval_id = response.json()["id"]

    response = client.post(
        f"/approvals/{approval_id}/decision",
        json={
            "approved": False,
            "decided_by": "human",
            "comment": "Not safe.",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["approval_id"] == approval_id
    assert body["approved"] is False
    assert body["decided_by"] == "human"
    assert body["comment"] == "Not safe."


def test_missing_approval_returns_404():
    response = client.get(f"/approvals/{uuid4()}")

    assert response.status_code == 404