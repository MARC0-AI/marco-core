from fastapi.testclient import TestClient

from marco.api.app import app

client = TestClient(app)


def test_app_exposes_approval_routes():
    response = client.get("/approvals/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json()["detail"] == "Approval not found"
