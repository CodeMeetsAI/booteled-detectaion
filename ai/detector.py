
"""
ai.detector — Object detection model wrapper.

Abstracts YOLO (or equivalent) object-detection inference: model
loading, per-frame ``detect()`` returning bounding boxes, class IDs,
and confidences, plus batching and GPU/CPU backend selection.
"""
