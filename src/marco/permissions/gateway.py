from marco.contracts.models import ApprovalRequest, ToolRequest
from marco.permissions.engine import PermissionDecision, PermissionResult


def create_approval_request(
    request: ToolRequest,
    result: PermissionResult,
) -> ApprovalRequest | None:
    if result.decision != PermissionDecision.ASK:
        return None

    return ApprovalRequest(
        task_id=request.task_id,
        tool_request_id=request.id,
        tool=request.tool,
        action=request.action,
        risk=request.risk,
        reason=result.reason.value,
        requires_human_approval=True,
        target=request.parameters.get("target"),
    )
