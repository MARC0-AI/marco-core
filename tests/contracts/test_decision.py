from uuid import uuid4

import pytest
from pydantic import ValidationError

from marco.contracts.models import ApprovalDecision


def test_approval_decision_accepts_approval():
    decision = ApprovalDecision(
        approval_id=uuid4(),
        approved=True,
        decided_by="human",
        comment="Looks safe.",
    )

    assert decision.approved is True
    assert decision.decided_by == "human"
    assert decision.comment == "Looks safe."


def test_approval_decision_requires_decider():
    with pytest.raises(ValidationError):
        ApprovalDecision(
            approval_id=uuid4(),
            approved=False,
            decided_by="",
        )
