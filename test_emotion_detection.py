"""Unit tests for the Emotion Detector."""

import unittest
from unittest.mock import Mock, patch

import requests

from emotion_detection import EmotionDetectionError, emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    """Tests input validation, response parsing, and service failures."""

    @patch("emotion_detection.requests.post")
    def test_returns_scores_and_dominant_emotion(self, post_mock: Mock) -> None:
        post_mock.return_value = Mock(
            status_code=200,
            json=lambda: {
                "emotionPredictions": [
                    {
                        "emotion": {
                            "anger": 0.05,
                            "disgust": 0.02,
                            "fear": 0.03,
                            "joy": 0.85,
                            "sadness": 0.05,
                        }
                    }
                ]
            },
        )
        post_mock.return_value.raise_for_status.return_value = None

        result = emotion_detector("I am glad this happened")

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["joy"], 0.85)
        self.assertEqual(set(result), {
            "anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"
        })

    def test_rejects_blank_input(self) -> None:
        with self.assertRaises(ValueError):
            emotion_detector("   ")

    @patch("emotion_detection.requests.post")
    def test_service_failure_is_reported(self, post_mock: Mock) -> None:
        post_mock.side_effect = requests.ConnectionError("offline")

        with self.assertRaises(EmotionDetectionError):
            emotion_detector("I am happy")

    @patch("emotion_detection.requests.post")
    def test_rejects_unexpected_response(self, post_mock: Mock) -> None:
        post_mock.return_value = Mock(
            status_code=200,
            json=lambda: {"unexpected": {}},
        )
        post_mock.return_value.raise_for_status.return_value = None

        with self.assertRaises(EmotionDetectionError):
            emotion_detector("I am happy")


if __name__ == "__main__":
    unittest.main()
