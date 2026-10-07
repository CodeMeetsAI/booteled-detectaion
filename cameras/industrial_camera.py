"""
cameras.industrial_camera — Industrial (GigE/PCIe) camera backend.

Concrete implementation of ``BaseCamera`` for machine-vision cameras
(e.g. Basler, FLIR/Point Grey).  Will manage SDK initialisation,
hardware triggering, and real-time frame acquisition at production
line speeds.
"""
