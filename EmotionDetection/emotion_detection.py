"""Emotion detection client for the Watson NLP service."""

import requests

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for the supplied text."""
    empty_result = {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }

    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return empty_result.copy()

    payload = {"raw_document": {"text": text_to_analyze}}
    try:
        response = requests.post(URL, json=payload, headers=HEADERS, timeout=20)
    except requests.RequestException:
        return empty_result.copy()

    if response.status_code == 400:
        return empty_result.copy()

    try:
        response.raise_for_status()
        emotions = response.json()["emotionPredictions"][0]["emotion"]
        dominant_emotion = max(emotions, key=emotions.get)
        return {
            "anger": emotions["anger"],
            "disgust": emotions["disgust"],
            "fear": emotions["fear"],
            "joy": emotions["joy"],
            "sadness": emotions["sadness"],
            "dominant_emotion": dominant_emotion,
        }
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        return empty_result.copy()
