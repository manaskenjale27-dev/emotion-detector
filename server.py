"""Flask web server for the Emotion Detector."""

from flask import Flask, jsonify, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def render_index_page():
    """Render the HTML interface."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_function():
    """Analyze supplied text and return emotion scores as JSON."""
    if request.method == "POST":
        text_to_analyze = request.form.get("textToAnalyze", "").strip()
    else:
        text_to_analyze = request.args.get("textToAnalyze", "").strip()

    if not text_to_analyze:
        return jsonify({"error": "Invalid text. Please enter text to analyze."}), 400

    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        return jsonify({"error": "Unable to analyze this text. Please try again."}), 400

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
