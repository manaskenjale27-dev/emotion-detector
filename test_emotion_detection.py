"""Unit tests for the EmotionDetection application."""

import json
import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Test formatted scores, dominant emotions, and HTTP 400 handling."""

    def make_response(self, scores, status_code=200):
        response = Mock()
        response.status_code = status_code
        response.text = json.dumps(
            {"emotionPredictions": [{"emotion": scores}]}
        )
        response.raise_for_status.return_value = None
        return response

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger_is_dominant(self, post_mock):
        post_mock.return_value = self.make_response({
            "anger": 0.8, "disgust": 0.1, "fear": 0.05,
            "joy": 0.02, "sadness": 0.03,
        })
        result = emotion_detector("I am angry")
        self.assertEqual(result["dominant_emotion"], "anger")
        self.assertEqual(set(result), {
            "anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"
        })

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_disgust_is_dominant(self, post_mock):
        post_mock.return_value = self.make_response({
            "anger": 0.02, "disgust": 0.88, "fear": 0.03,
            "joy": 0.02, "sadness": 0.05,
        })
        self.assertEqual(
            emotion_detector("That is disgusting")["dominant_emotion"],
            "disgust",
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_fear_is_dominant(self, post_mock):
        post_mock.return_value = self.make_response({
            "anger": 0.02, "disgust": 0.03, "fear": 0.88,
            "joy": 0.02, "sadness": 0.05,
        })
        self.assertEqual(
            emotion_detector("I am afraid")["dominant_emotion"], "fear"
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_joy_is_dominant(self, post_mock):
        post_mock.return_value = self.make_response({
            "anger": 0.02, "disgust": 0.03, "fear": 0.05,
            "joy": 0.8, "sadness": 0.1,
        })
        self.assertEqual(
            emotion_detector("I am happy")["dominant_emotion"], "joy"
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sadness_is_dominant(self, post_mock):
        post_mock.return_value = self.make_response({
            "anger": 0.02, "disgust": 0.03, "fear": 0.05,
            "joy": 0.1, "sadness": 0.8,
        })
        self.assertEqual(
            emotion_detector("I am sad")["dominant_emotion"], "sadness"
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_none_values(self, post_mock):
        post_mock.return_value = Mock(status_code=400)
        self.assertEqual(
            emotion_detector("invalid input"),
            {
                "anger": None, "disgust": None, "fear": None,
                "joy": None, "sadness": None, "dominant_emotion": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
