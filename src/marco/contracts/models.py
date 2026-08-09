from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    goal: str = Field(min_length=1)
    status: TaskStatus = TaskStatus.PENDING
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    tool: str = Field(min_length=1)
    action: str = Field(min_length=1)
    parameters: dict[str, Any] = Field(default_factory=dict)
    risk: RiskLevel = RiskLevel.LOW


class PermissionRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    tool_request_id: UUID
    reason: str = Field(min_length=1)
    risk: RiskLevel
    approved: bool | None = None


class ApprovalRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    tool_request_id: UUID
    tool: str = Field(min_length=1)
    action: str = Field(min_length=1)
    risk: RiskLevel
    reason: str = Field(min_length=1)
    requires_human_approval: bool = True
    target: str | None = None


class ExecutionResult(BaseModel):
    success: bool
    output: Any = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
