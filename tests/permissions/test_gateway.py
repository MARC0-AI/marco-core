from uuid import uuid4

from marco.contracts.models import RiskLevel, ToolRequest
from marco.permissions.engine import PermissionDecision, PermissionEngine
from marco.permissions.gateway import create_approval_request


def make_request(action: str, risk: RiskLevel) -> ToolRequest:
    return ToolRequest(
        task_id=uuid4(),
        tool="filesystem",
        action=action,
        risk=risk,
        parameters={"target": "/tmp/example.txt"},
    )


def test_ask_creates_approval_request():
    request = make_request("delete", RiskLevel.LOW)
    result = PermissionEngine().evaluate(request)

    approval = create_approval_request(request, result)

    assert result.decision == PermissionDecision.ASK
    assert approval is not None
    assert approval.tool == "filesystem"
    assert approval.action == "delete"
    assert approval.risk == RiskLevel.LOW
    assert approval.requires_human_approval is True
    assert approval.target == "/tmp/example.txt"


def test_allow_does_not_create_approval_request():
    request = make_request("read", RiskLevel.LOW)
    result = PermissionEngine().evaluate(request)

    approval = create_approval_request(request, result)

    assert result.decision == PermissionDecision.ALLOW
    assert approval is None
