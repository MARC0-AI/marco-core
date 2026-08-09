from enum import StrEnum
from typing import ClassVar

from marco.contracts.models import RiskLevel, ToolRequest


class PermissionDecision(StrEnum):
    ALLOW = "allow"
    ASK = "ask"
    DENY = "deny"


class PermissionEngine:
    """Deterministic safety gate for MARCO tool requests."""

    SENSITIVE_ACTIONS: ClassVar[set[str]] = {
        "delete",
        "send",
        "push",
        "deploy",
        "shutdown",
        "restart",
        "sudo",
        "change_system_settings",
    }

    def evaluate(self, request: ToolRequest) -> PermissionDecision:
        action = request.action.lower().strip()

        if action in self.SENSITIVE_ACTIONS:
            return PermissionDecision.ASK

        if request.risk == RiskLevel.LOW:
            return PermissionDecision.ALLOW

        if request.risk in {RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL}:
            return PermissionDecision.ASK

        return PermissionDecision.ASK
