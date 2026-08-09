from uuid import uuid4

import pytest
from pydantic import ValidationError

from marco.contracts.models import (
    ExecutionResult,
    PermissionRequest,
    RiskLevel,
    Task,
    TaskStatus,
    ToolRequest,
)


def test_task_defaults():
    task = Task(goal="Create a Python file")

    assert task.goal == "Create a Python file"
    assert task.status == TaskStatus.PENDING
    assert task.id


def test_tool_request():
    task_id = uuid4()

    request = ToolRequest(
        task_id=task_id,
        tool="terminal",
        action="run",
        parameters={"command": "python app.py"},
        risk=RiskLevel.MEDIUM,
    )

    assert request.task_id == task_id
    assert request.tool == "terminal"


def test_permission_starts_undecided():
    task_id = uuid4()
    tool_request_id = uuid4()

    request = PermissionRequest(
        task_id=task_id,
        tool_request_id=tool_request_id,
        reason="Run a terminal command",
        risk=RiskLevel.HIGH,
    )

    assert request.approved is None


def test_execution_result():
    result = ExecutionResult(
        success=True,
        output="Hello MARCO",
    )

    assert result.success
    assert result.output == "Hello MARCO"


def test_task_requires_goal():
    with pytest.raises(ValidationError):
        Task(goal="")


def test_permission_can_be_approved():
    request = PermissionRequest(
        task_id=uuid4(),
        tool_request_id=uuid4(),
        reason="Send an email",
        risk=RiskLevel.HIGH,
        approved=True,
    )

    assert request.approved is True


def test_permission_rejects_invalid_approval():
    with pytest.raises(ValidationError):
        PermissionRequest(
            task_id=uuid4(),
            tool_request_id=uuid4(),
            reason="Send an email",
            risk=RiskLevel.HIGH,
            approved="maybe",
        )
