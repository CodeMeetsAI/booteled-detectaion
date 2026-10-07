"""
Deterministic inspection decision rules.

This module converts individual inspection checks into
a final PASS / FAIL / UNCERTAIN / SYSTEM_FAULT decision.
"""

from decision.result import InspectionResult, InspectionStatus


# Defects that must always cause a bottle to FAIL.
CRITICAL_DEFECT_CODES = {
    "CAP_MISSING",
    "CAP_TILTED",
    "CAP_MISALIGNED",
    "CAP_NOT_SEATED",
    "LOW_FILL",
    "HIGH_FILL",
    "LABEL_MISSING",
    "LABEL_MISALIGNED",
    "PACKAGING_FAULT",
    "TAMPER_FAULT",
    "OCR_FAIL",
}


# Conditions where the system cannot safely confirm the bottle.
UNCERTAIN_CODES = {
    "FILL_UNCERTAIN",
    "INSPECTION_UNCERTAIN",
}


def evaluate_result(result: InspectionResult) -> InspectionResult:
    """
    Evaluate an inspection result and assign its final status.

    Rules:
    1. System faults have highest priority.
    2. Critical defects cause FAIL.
    3. Uncertain inspection conditions cause UNCERTAIN.
    4. No problems means PASS.

    Multiple defects are preserved.
    """

    defect_codes = set(result.defect_codes)

    # System fault has the highest priority.
    if "SYSTEM_FAULT" in defect_codes:
        result.status = InspectionStatus.SYSTEM_FAULT
        return result

    # Any critical production defect causes FAIL.
    if defect_codes.intersection(CRITICAL_DEFECT_CODES):
        result.status = InspectionStatus.FAIL
        return result

    # If the system cannot confidently inspect the bottle,
    # do not silently pass it.
    if defect_codes.intersection(UNCERTAIN_CODES):
        result.status = InspectionStatus.UNCERTAIN
        return result

    # No defects = PASS.
    result.status = InspectionStatus.PASS

    return result