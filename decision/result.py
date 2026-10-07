"""
Standardized inspection result models.

This module defines the data structures used to represent
the result of a bottle inspection.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class InspectionStatus(str, Enum):
    """Final status of a bottle inspection."""

    PASS = "PASS"
    FAIL = "FAIL"
    UNCERTAIN = "UNCERTAIN"
    SYSTEM_FAULT = "SYSTEM_FAULT"


@dataclass
class DefectResult:
    """Represents one detected defect."""

    code: str
    confidence: float | None = None
    severity: str = "MEDIUM"
    message: str = ""


@dataclass
class InspectionResult:
    """
    Complete result of inspecting one bottle.

    The decision engine will later use this structure to
    produce the final PASS/FAIL/UNCERTAIN decision.
    """

    status: InspectionStatus = InspectionStatus.UNCERTAIN

    # Bottle identification
    bottle_sequence: int | None = None
    camera_id: str = ""

    # Inspection measurements
    cap_present: bool | None = None
    cap_seated: bool | None = None

    fill_status: str | None = None
    fill_measurement_ml: float | None = None

    packaging_status: str | None = None
    tamper_status: str | None = None
    ocr_status: str | None = None

    # Defects detected during inspection
    defects: list[DefectResult] = field(default_factory=list)

    # Performance / model information
    processing_ms: float = 0.0
    model_version: str | None = None
    recipe_version: str | None = None

    # Optional additional information
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_defect(
        self,
        code: str,
        confidence: float | None = None,
        severity: str = "MEDIUM",
        message: str = "",
    ) -> None:
        """Add a defect to the inspection result."""

        self.defects.append(
            DefectResult(
                code=code,
                confidence=confidence,
                severity=severity,
                message=message,
            )
        )

    @property
    def passed(self) -> bool:
        """Return True when the final inspection status is PASS."""

        return self.status == InspectionStatus.PASS

    @property
    def failed(self) -> bool:
        """Return True when the final inspection status is FAIL."""

        return self.status == InspectionStatus.FAIL

    @property
    def uncertain(self) -> bool:
        """Return True when the inspection is uncertain."""

        return self.status == InspectionStatus.UNCERTAIN

    @property
    def system_fault(self) -> bool:
        """Return True when a system fault occurred."""

        return self.status == InspectionStatus.SYSTEM_FAULT

    @property
    def defect_codes(self) -> list[str]:
        """Return all defect codes detected for this bottle."""

        return [defect.code for defect in self.defects]