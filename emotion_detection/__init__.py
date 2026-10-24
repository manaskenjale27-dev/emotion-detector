"""Public interface for the emotion detection package."""

from .emotion_detection import EmotionDetectionError, emotion_detector

__all__ = ["EmotionDetectionError", "emotion_detector"]
