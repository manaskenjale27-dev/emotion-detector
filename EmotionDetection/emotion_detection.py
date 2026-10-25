import json

import requests

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}


class EmotionDetectionError(RuntimeError):
    """Raised when the emotion detection service fails."""


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the dominant emotion."""
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
        response = requests.post(URL, json=payload, headers=HEADERS)
    except requests.RequestException as exc:
        raise EmotionDetectionError("The emotion service request failed.") from exc

    if response.status_code == 400:
        return empty_result.copy()

    try:
        response.raise_for_status()
        data = json.loads(response.text)
        emotions = data["emotionPredictions"][0]["emotion"]
        dominant_emotion = max(emotions, key=emotions.get)
        return {
            "anger": emotions["anger"],
            "disgust": emotions["disgust"],
            "fear": emotions["fear"],
            "joy": emotions["joy"],
            "sadness": emotions["sadness"],
            "dominant_emotion": dominant_emotion,
        }
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as exc:
        raise EmotionDetectionError("The emotion service returned an invalid response.") from exc
