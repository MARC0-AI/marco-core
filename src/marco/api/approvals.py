from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from marco.contracts.models import ApprovalDecision, ApprovalRequest


class ApprovalStatus(str):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"


class ApprovalRecord(BaseModel):
    id: UUID
    request: ApprovalRequest
    status: str = ApprovalStatus.PENDING


class DecisionInput(BaseModel):
    approved: bool
    decided_by: str
    comment: str | None = None


router = APIRouter(prefix="/approvals", tags=["approvals"])
_store: dict[UUID, ApprovalRecord] = {}


@router.post("", response_model=ApprovalRecord, status_code=201)
def create_approval(request: ApprovalRequest) -> ApprovalRecord:
    record = ApprovalRecord(id=uuid4(), request=request)
    _store[record.id] = record
    return record


@router.get("/{approval_id}", response_model=ApprovalRecord)
def get_approval(approval_id: UUID) -> ApprovalRecord:
    if approval_id not in _store:
        raise HTTPException(status_code=404, detail="Approval not found")
    return _store[approval_id]


@router.post("/{approval_id}/decision", response_model=ApprovalDecision)
def decide_approval(
    approval_id: UUID,
    decision: DecisionInput,
) -> ApprovalDecision:
    record = _store.get(approval_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Approval not found")

    record.status = (
        ApprovalStatus.APPROVED if decision.approved else ApprovalStatus.DENIED
    )

    return ApprovalDecision(
        approval_id=approval_id,
        approved=decision.approved,
        decided_by=decision.decided_by,
        comment=decision.comment,
    )

