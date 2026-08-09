from uuid import uuid4

from marco.contracts.models import ApprovalRequest, RiskLevel


def test_approval_request_defaults_to_human_approval():
    request = ApprovalRequest(
        task_id=uuid4(),
        tool_request_id=uuid4(),
        tool="browser",
        action="send",
        risk=RiskLevel.HIGH,
        reason="sensitive_action",
    )

    assert request.requires_human_approval is True
    assert request.target is None


def test_approval_request_accepts_target():
    request = ApprovalRequest(
        task_id=uuid4(),
        tool_request_id=uuid4(),
        tool="browser",
        action="send",
        risk=RiskLevel.HIGH,
        reason="sensitive_action",
        target="example.com",
    )

    assert request.target == "example.com"
