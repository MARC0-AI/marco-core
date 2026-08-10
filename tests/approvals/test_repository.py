from uuid import uuid4

from marco.api.approvals import ApprovalRecord
from marco.approvals.repository import InMemoryApprovalRepository


def make_record() -> ApprovalRecord:
    return ApprovalRecord(
        id=uuid4(),
        request={
            "task_id": uuid4(),
            "tool_request_id": uuid4(),
            "tool": "browser",
            "action": "send",
            "risk": "high",
            "reason": "sensitive_action",
            "requires_human_approval": True,
        },
    )


def test_save_and_get():
    repository = InMemoryApprovalRepository()
    record = make_record()

    repository.save(record)

    assert repository.get(record.id) == record


def test_missing_approval_returns_none():
    repository = InMemoryApprovalRepository()

    assert repository.get(uuid4()) is None


def test_update_replaces_record():
    repository = InMemoryApprovalRepository()
    record = make_record()
    repository.save(record)

    record.status = "approved"
    repository.update(record)

    assert repository.get(record.id).status == "approved"