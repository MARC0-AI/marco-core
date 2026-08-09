from uuid import uuid4

from marco.contracts.models import RiskLevel, ToolRequest
from marco.permissions import PermissionDecision, PermissionEngine, PermissionReason


def request(action: str, risk: RiskLevel) -> ToolRequest:
    return ToolRequest(
        task_id=uuid4(),
        tool="filesystem",
        action=action,
        risk=risk,
    )


def test_low_risk_action_is_allowed():
    engine = PermissionEngine()

    result = engine.evaluate(request("read", RiskLevel.LOW))

    assert result.decision == PermissionDecision.ALLOW


def test_medium_risk_requires_approval():
    engine = PermissionEngine()

    result = engine.evaluate(request("run", RiskLevel.MEDIUM))

    assert result.decision == PermissionDecision.ASK


def test_high_risk_requires_approval():
    engine = PermissionEngine()

    result = engine.evaluate(request("edit", RiskLevel.HIGH))

    assert result.decision == PermissionDecision.ASK


def test_critical_risk_requires_approval():
    engine = PermissionEngine()

    result = engine.evaluate(request("anything", RiskLevel.CRITICAL))

    assert result.decision == PermissionDecision.ASK


def test_delete_always_requires_approval():
    engine = PermissionEngine()

    result = engine.evaluate(request("delete", RiskLevel.LOW))

    assert result.decision == PermissionDecision.ASK


def test_send_always_requires_approval():
    engine = PermissionEngine()

    result = engine.evaluate(request("send", RiskLevel.LOW))

    assert result.decision == PermissionDecision.ASK


def test_push_requires_approval():
    engine = PermissionEngine()

    result = engine.evaluate(request("push", RiskLevel.LOW))

    assert result.decision == PermissionDecision.ASK


def test_sensitive_action_has_sensitive_reason():
    result = PermissionEngine().evaluate(request("delete", RiskLevel.LOW))

    assert result.decision == PermissionDecision.ASK
    assert result.reason == PermissionReason.SENSITIVE_ACTION


def test_low_risk_action_has_safe_reason():
    result = PermissionEngine().evaluate(request("read", RiskLevel.LOW))

    assert result.decision == PermissionDecision.ALLOW
    assert result.reason == PermissionReason.SAFE_ACTION