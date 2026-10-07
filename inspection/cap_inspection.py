"""
Cap inspection utilities.

The cap inspection layer determines whether a bottle cap is:
- present
- seated correctly
- potentially tilted or misaligned

The implementation is intentionally lightweight and CPU-friendly.
AI detection can be integrated later without changing the result structure.
"""

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class CapInspectionConfig:
    """Configuration for cap inspection."""

    # Minimum percentage of dark/edge structure expected
    # in the cap inspection region.
    min_edge_density: float = 0.01

    # Allowed horizontal/vertical position deviation
    # when geometry-based inspection is used.
    max_position_deviation: float = 0.20

    # Maximum allowed tilt angle in degrees.
    max_tilt_angle: float = 8.0


@dataclass
class CapInspectionResult:
    """Result produced by the cap inspection."""

    cap_present: bool
    cap_seated: bool
    cap_tilted: bool = False
    cap_misaligned: bool = False
    confidence: float = 0.0
    message: str = ""


def calculate_edge_density(frame: np.ndarray) -> float:
    """
    Calculate edge density in an image.

    Edge density is used only as a lightweight visual signal.
    It is NOT a replacement for a trained AI detector.
    """

    if frame is None or frame.size == 0:
        raise ValueError("Input frame is empty")

    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame

    edges = cv2.Canny(gray, 50, 150)

    total_pixels = edges.shape[0] * edges.shape[1]

    if total_pixels == 0:
        return 0.0

    edge_pixels = np.count_nonzero(edges)

    return float(edge_pixels / total_pixels)


def inspect_cap_presence(
    frame: np.ndarray,
    config: CapInspectionConfig | None = None,
) -> CapInspectionResult:
    """
    Perform a basic cap-presence inspection.

    This is a baseline detector intended for pipeline testing.
    Real production detection will later use camera-specific
    ROI geometry and/or a trained detector.
    """

    if config is None:
        config = CapInspectionConfig()

    density = calculate_edge_density(frame)

    cap_present = density >= config.min_edge_density

    if cap_present:
        return CapInspectionResult(
            cap_present=True,
            cap_seated=True,
            confidence=min(density / 0.10, 1.0),
            message="Cap visual structure detected.",
        )

    return CapInspectionResult(
        cap_present=False,
        cap_seated=False,
        confidence=1.0 - min(density / 0.01, 1.0),
        message="Cap visual structure not detected.",
    )


def inspect_cap(
    frame: np.ndarray,
    config: CapInspectionConfig | None = None,
) -> CapInspectionResult:
    """
    Run the complete baseline cap inspection.

    Currently this performs cap-presence analysis.
    Geometry-based seating/tilt analysis will be added once
    the actual camera ROI and bottle geometry are established.
    """

    return inspect_cap_presence(frame, config)