from enum import StrEnum

from marco.contracts.models import RiskLevel


class PermissionReason(StrEnum):
    SAFE_ACTION = "safe_action"
    SENSITIVE_ACTION = "sensitive_action"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"
    CRITICAL_RISK = "critical_risk"


def reason_for(action: str, risk: RiskLevel, sensitive: bool) -> PermissionReason:
    if sensitive:
        return PermissionReason.SENSITIVE_ACTION

    return {
        RiskLevel.LOW: PermissionReason.SAFE_ACTION,
        RiskLevel.MEDIUM: PermissionReason.MEDIUM_RISK,
        RiskLevel.HIGH: PermissionReason.HIGH_RISK,
        RiskLevel.CRITICAL: PermissionReason.CRITICAL_RISK,
    }[risk]
