from typing import Protocol
from uuid import UUID

from marco.api.approvals import ApprovalRecord


class ApprovalRepository(Protocol):
    def save(self, record: ApprovalRecord) -> ApprovalRecord: ...

    def get(self, approval_id: UUID) -> ApprovalRecord | None: ...

    def update(self, record: ApprovalRecord) -> ApprovalRecord: ...


class InMemoryApprovalRepository:
    def __init__(self) -> None:
        self._store: dict[UUID, ApprovalRecord] = {}

    def save(self, record: ApprovalRecord) -> ApprovalRecord:
        self._store[record.id] = record
        return record

    def get(self, approval_id: UUID) -> ApprovalRecord | None:
        return self._store.get(approval_id)

    def update(self, record: ApprovalRecord) -> ApprovalRecord:
        self._store[record.id] = record
        return record