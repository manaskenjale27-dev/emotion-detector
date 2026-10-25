"""Flask web server for the Emotion Detector."""

import subprocess

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_detector_function():
    """Analyze the submitted text and format emotion scores."""
    text_to_analyze = request.args.get("textToAnalyze")
    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        response_text = "Invalid Input! Please try again."
    else:
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
            f"'fear': {response['fear']}, 'joy': {response['joy']}, "
            f"'sadness': {response['sadness']}. The dominant emotion is "
            f"{response['dominant_emotion']}."
        )

    return response_text


@app.route("/")
def render_index_page():
    """Render the HTML interface."""
    return render_template("index.html")


if __name__ == "__main__":
    analysis = subprocess.run(
        ["python3", "-m", "pylint", "server.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    print(analysis.stdout)
    print(analysis.stderr)
    app.run(host="0.0.0.0", port=5000, debug=False)
