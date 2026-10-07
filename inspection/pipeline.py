"""
inspection.pipeline — Inspection orchestration.

Coordinates the full per-bottle workflow: image acquisition,
pre-processing, sequential execution of individual inspection modules
(cap, fill-level, packaging, OCR), aggregation of results, and
hand-off to the decision engine for the final PASS/FAIL verdict.
"""
