from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal
from enum import Enum

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Status(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

class FlowData(BaseModel):
    src_ip: str
    dst_ip: str
    src_port: int = Field(ge=0, le=65535)
    dst_port: int = Field(ge=0, le=65535)
    protocol: Literal["TCP", "UDP", "ICMP", "OTHER"] = "TCP"
    packet_size: float = Field(gt=0)
    duration: float = Field(ge=0)
    packet_count: int = Field(ge=1)
    byte_count: int = Field(ge=0)
    flags: Optional[str] = None

class Prediction(BaseModel):
    flow_id: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    anomaly_score: float = Field(ge=0.0, le=1.0)
    is_anomaly: bool
    confidence: float = Field(ge=0.0, le=1.0)

class Alert(BaseModel):
    alert_id: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: Severity
    source_ip: str
    destination_ip: str
    alert_type: str
    description: str
    anomaly_score: float = Field(ge=0.0, le=1.0)
    status: Status = Status.OPEN