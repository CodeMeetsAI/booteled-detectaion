"""
Database models for the Pharma Bottle Vision System.

The database stores:
- Products
- Inspection recipes
- Production batches
- Bottle inspections
- Defects
- Evidence files
- System events
- Audit logs
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


class BatchStatus(str, Enum):
    """Production batch lifecycle states."""

    CREATED = "CREATED"
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"


class InspectionResult(str, Enum):
    """Final inspection result."""

    PASS = "PASS"
    FAIL = "FAIL"
    UNCERTAIN = "UNCERTAIN"
    SYSTEM_FAULT = "SYSTEM_FAULT"


class Product(SQLModel, table=True):
    """Product configuration."""

    id: Optional[int] = Field(default=None, primary_key=True)

    product_code: str = Field(index=True, unique=True)
    product_name: str

    target_fill_ml: float
    fill_tolerance_ml: float

    cap_profile: str
    label_profile: str

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Recipe(SQLModel, table=True):
    """Versioned inspection recipe."""

    id: Optional[int] = Field(default=None, primary_key=True)

    product_id: int = Field(index=True)

    version: str

    cap_inspection_enabled: bool = True
    fill_level_inspection_enabled: bool = True
    packaging_inspection_enabled: bool = True
    tamper_ring_inspection_enabled: bool = True
    ocr_enabled: bool = False

    cap_confidence_threshold: float = 0.50
    label_confidence_threshold: float = 0.50
    tamper_confidence_threshold: float = 0.50
    packaging_confidence_threshold: float = 0.50

    created_at: datetime = Field(default_factory=utc_now)


class Batch(SQLModel, table=True):
    """Production batch."""

    id: Optional[int] = Field(default=None, primary_key=True)

    batch_number: str = Field(index=True, unique=True)

    product_id: int = Field(index=True)
    recipe_id: int = Field(index=True)

    expected_quantity: int

    processed_quantity: int = 0
    passed_quantity: int = 0
    rejected_quantity: int = 0

    status: BatchStatus = BatchStatus.CREATED

    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=utc_now)


class Inspection(SQLModel, table=True):
    """Inspection result for one bottle."""

    id: Optional[int] = Field(default=None, primary_key=True)

    batch_id: int = Field(index=True)

    bottle_sequence: int = Field(index=True)

    timestamp: datetime = Field(default_factory=utc_now)

    camera_id: str

    result: InspectionResult

    processing_ms: float

    model_version: Optional[str] = None
    recipe_version: Optional[str] = None

    cap_present: Optional[bool] = None
    cap_seated: Optional[bool] = None

    fill_status: Optional[str] = None
    fill_measurement_ml: Optional[float] = None

    packaging_status: Optional[str] = None
    tamper_status: Optional[str] = None
    ocr_status: Optional[str] = None


class Defect(SQLModel, table=True):
    """Individual defect detected during an inspection."""

    id: Optional[int] = Field(default=None, primary_key=True)

    inspection_id: int = Field(index=True)

    defect_code: str = Field(index=True)

    confidence: Optional[float] = None

    severity: Optional[str] = None

    created_at: datetime = Field(default_factory=utc_now)


class Evidence(SQLModel, table=True):
    """Image evidence associated with an inspection."""

    id: Optional[int] = Field(default=None, primary_key=True)

    inspection_id: int = Field(index=True)

    original_image: Optional[str] = None
    annotated_image: Optional[str] = None

    created_at: datetime = Field(default_factory=utc_now)


class SystemEvent(SQLModel, table=True):
    """System-level operational event."""

    id: Optional[int] = Field(default=None, primary_key=True)

    event_type: str = Field(index=True)

    message: str

    severity: str = "INFO"

    created_at: datetime = Field(default_factory=utc_now)


class AuditLog(SQLModel, table=True):
    """Audit trail for important configuration changes."""

    id: Optional[int] = Field(default=None, primary_key=True)

    user: str

    action: str

    entity_type: str

    entity_id: Optional[int] = None

    details: Optional[str] = None

    created_at: datetime = Field(default_factory=utc_now)