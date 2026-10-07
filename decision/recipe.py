"""
Inspection recipe configuration.

A recipe defines how a particular product should be inspected.
Different products can have different inspection requirements
and confidence thresholds.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class InspectionRecipe:
    """Configuration for one inspection recipe."""

    product_code: str
    version: str

    # Inspection switches
    cap_inspection_enabled: bool = True
    fill_level_inspection_enabled: bool = True
    packaging_inspection_enabled: bool = True
    tamper_ring_inspection_enabled: bool = True
    ocr_enabled: bool = False

    # AI confidence thresholds
    cap_confidence_threshold: float = 0.50
    label_confidence_threshold: float = 0.50
    tamper_confidence_threshold: float = 0.50
    packaging_confidence_threshold: float = 0.50

    # Fill-level settings
    target_fill_ml: float = 100.0
    fill_tolerance_ml: float = 2.0

    def validate(self) -> None:
        """Validate recipe configuration."""

        thresholds = {
            "cap_confidence_threshold": self.cap_confidence_threshold,
            "label_confidence_threshold": self.label_confidence_threshold,
            "tamper_confidence_threshold": self.tamper_confidence_threshold,
            "packaging_confidence_threshold": self.packaging_confidence_threshold,
        }

        for name, value in thresholds.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{name} must be between 0.0 and 1.0"
                )

        if self.target_fill_ml <= 0:
            raise ValueError("target_fill_ml must be greater than 0")

        if self.fill_tolerance_ml < 0:
            raise ValueError("fill_tolerance_ml cannot be negative")

        if not self.product_code.strip():
            raise ValueError("product_code cannot be empty")

        if not self.version.strip():
            raise ValueError("recipe version cannot be empty")