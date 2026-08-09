from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar

from marco.contracts.models import RiskLevel, ToolRequest
from marco.permissions.reasons import PermissionReason, reason_for


class PermissionDecision(StrEnum):
    ALLOW = "allow"
    ASK = "ask"
    DENY = "deny"



@dataclass(frozen=True, slots=True)
class PermissionResult:
    decision: PermissionDecision
    reason: PermissionReason

class PermissionEngine:
    SENSITIVE_ACTIONS: ClassVar[set[str]] = {
        "delete", "send", "push", "deploy",
        "shutdown", "restart", "sudo",
        "change_system_settings",
    }

    def evaluate(self, request: ToolRequest) -> PermissionResult:
        action = request.action.lower().strip()
        sensitive = action in self.SENSITIVE_ACTIONS

        if sensitive or request.risk != RiskLevel.LOW:
            decision = PermissionDecision.ASK
        else:
            decision = PermissionDecision.ALLOW

        return PermissionResult(
            decision,
            reason_for(action, request.risk, sensitive),
        )