"""Analyze text with the IBM Skills Network emotion prediction service."""

import json

import requests

EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "accenture-watson-nlp-bert-emotion-mp-vocab-desktop"


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the dominant emotion.

    Blank input and HTTP 400 responses return None values for every score.
    Network and unexpected service errors are reported as clear exceptions.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    payload = {"raw_document": {"text": text_to_analyze}}
    headers = {"grpc-metadata-mm-model-id": MODEL_ID}

    response = requests.post(EMOTION_URL, json=payload, headers=headers)

    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    response.raise_for_status()
    formatted_response = json.loads(response.text)
    emotions = formatted_response["emotionPredictions"][0]["emotion"]
    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
        "dominant_emotion": dominant_emotion,
    }
