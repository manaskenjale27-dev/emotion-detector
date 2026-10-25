"""Flask web server for the Emotion Detector."""

import os

from flask import Flask, jsonify, render_template, request

from emotion_detection import EmotionDetectionError, emotion_detector

app = Flask(__name__)


@app.get("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def detect_emotion():
    """Analyze submitted text and return the emotion scores."""
    text_to_analyze = (
        request.form.get("textToAnalyze", "")
        or request.args.get("textToAnalyze", "")
    ).strip()
    if not text_to_analyze:
        return jsonify({"error": "Please enter text to analyze."}), 400

    try:
        result = emotion_detector(text_to_analyze)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except EmotionDetectionError as exc:
        return jsonify({"error": str(exc)}), 502

    return jsonify(result)


@app.errorhandler(404)
def not_found(_error):
    """Return JSON for unknown routes."""
    return jsonify({"error": "Route not found."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=False)
