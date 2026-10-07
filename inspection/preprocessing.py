"""
Image preprocessing utilities for bottle inspection.

This module contains lightweight CPU-friendly preprocessing
operations that can be used before AI or classical CV inspection.
"""

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class PreprocessingConfig:
    """Configuration for image preprocessing."""

    target_width: int = 640
    target_height: int = 480

    # Optional region of interest.
    # Format: (x, y, width, height)
    roi: tuple[int, int, int, int] | None = None

    # Image enhancement
    brightness: int = 0
    contrast: float = 1.0

    # Whether to convert the final image to RGB.
    convert_to_rgb: bool = False


def resize_frame(
    frame: np.ndarray,
    width: int,
    height: int,
) -> np.ndarray:
    """
    Resize a frame to the requested dimensions.

    INTER_AREA is used because it is generally suitable
    for reducing camera image resolution.
    """

    if frame is None or frame.size == 0:
        raise ValueError("Input frame is empty")

    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be greater than zero")

    return cv2.resize(
        frame,
        (width, height),
        interpolation=cv2.INTER_AREA,
    )


def crop_roi(
    frame: np.ndarray,
    roi: tuple[int, int, int, int] | None,
) -> np.ndarray:
    """
    Crop a region of interest from a frame.

    ROI format:
        (x, y, width, height)

    If ROI is None, the original frame is returned.
    """

    if frame is None or frame.size == 0:
        raise ValueError("Input frame is empty")

    if roi is None:
        return frame

    x, y, width, height = roi

    if width <= 0 or height <= 0:
        raise ValueError("ROI width and height must be greater than zero")

    frame_height, frame_width = frame.shape[:2]

    if x < 0 or y < 0:
        raise ValueError("ROI x and y cannot be negative")

    if x + width > frame_width:
        raise ValueError("ROI exceeds frame width")

    if y + height > frame_height:
        raise ValueError("ROI exceeds frame height")

    return frame[y:y + height, x:x + width]


def adjust_brightness_contrast(
    frame: np.ndarray,
    brightness: int = 0,
    contrast: float = 1.0,
) -> np.ndarray:
    """
    Adjust brightness and contrast.

    brightness:
        -255 to 255

    contrast:
        Positive floating-point multiplier.
        1.0 means no change.
    """

    if frame is None or frame.size == 0:
        raise ValueError("Input frame is empty")

    if not -255 <= brightness <= 255:
        raise ValueError("Brightness must be between -255 and 255")

    if contrast <= 0:
        raise ValueError("Contrast must be greater than zero")

    adjusted = cv2.convertScaleAbs(
        frame,
        alpha=contrast,
        beta=brightness,
    )

    return adjusted


def preprocess_frame(
    frame: np.ndarray,
    config: PreprocessingConfig | None = None,
) -> np.ndarray:
    """
    Run the complete preprocessing pipeline.

    Pipeline:
        1. Resize
        2. Crop ROI
        3. Brightness/contrast adjustment
        4. Optional BGR → RGB conversion
    """

    if config is None:
        config = PreprocessingConfig()

    processed = resize_frame(
        frame,
        config.target_width,
        config.target_height,
    )

    processed = crop_roi(
        processed,
        config.roi,
    )

    processed = adjust_brightness_contrast(
        processed,
        brightness=config.brightness,
        contrast=config.contrast,
    )

    if config.convert_to_rgb:
        processed = cv2.cvtColor(
            processed,
            cv2.COLOR_BGR2RGB,
        )

    return processed