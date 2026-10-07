
"""
ai.model_manager — Central model lifecycle manager.

Handles discovery, loading, caching, warm-up, and version selection
of detection and segmentation models.  Ensures the correct model is
loaded once and shared across inspection threads for throughput.
"""
