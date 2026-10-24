"""Emotion detection client for the IBM Watson NLP service."""

import os
from typing import Any

import requests

EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")
DEFAULT_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
DEFAULT_TIMEOUT = 15


class EmotionDetectionError(RuntimeError):
    """Raised when the emotion service cannot analyze the supplied text."""


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Return five emotion scores and the dominant emotion for the text.

    Configure WATSON_EMOTION_URL to use the endpoint supplied by your course.
    This endpoint may require an X-IBM-NLP-Language header and the documented
    application/json request shape used by the IBM Skills Network lab.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        raise ValueError("Please enter text to analyze.")

    url = os.getenv("WATSON_EMOTION_URL", DEFAULT_URL)
    payload = {"raw_document": {"text": text_to_analyze.strip()}}
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise EmotionDetectionError(
            "The emotion service is unavailable. Check the endpoint and your connection."
        ) from exc
    except ValueError as exc:
        raise EmotionDetectionError(
            "The emotion service returned invalid JSON."
        ) from exc

    scores = _extract_scores(data)
    dominant = max(EMOTION_KEYS, key=scores.__getitem__)
    return {**scores, "dominant_emotion": dominant}


def _extract_scores(data: dict[str, Any]) -> dict[str, float]:
    """Extract emotion scores from the Watson response formats used in labs."""
    candidates = [
        data.get("emotionPredictions", [{}])[0].get("emotion", {}),
        data.get("emotion", {}),
        data.get("emotions", {}),
    ]
    emotion_data = next(
        (candidate for candidate in candidates if all(key in candidate for key in EMOTION_KEYS)),
        None,
    )
    if not isinstance(emotion_data, dict):
        raise EmotionDetectionError(
            "The emotion service response did not contain the expected five emotion scores."
        )

    try:
        scores = {key: float(emotion_data[key]) for key in EMOTION_KEYS}
    except (TypeError, ValueError) as exc:
        raise EmotionDetectionError(
            "The emotion service returned invalid emotion scores."
        ) from exc

    if any(not 0.0 <= score <= 1.0 for score in scores.values()):
        raise EmotionDetectionError(
            "The emotion service returned scores outside the expected 0 to 1 range."
        )
    return scores
