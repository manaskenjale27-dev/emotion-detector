# Emotion Detector

A Flask web app for analyzing text with IBM Watson NLP emotion prediction. It reports anger, disgust, fear, joy, sadness, and the dominant emotion.

## Project structure

```text
emotion-detector/
├── emotion_detection/
│   ├── __init__.py
│   └── emotion_detection.py
├── server.py
├── test_emotion_detection.py
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- Internet access to the emotion prediction service
- The endpoint specified by your IBM/Coursera lab, if it differs from the default

## Run locally on macOS or Linux

```bash
git clone https://github.com/manaskenjale27-dev/emotion-detector.git
cd emotion-detector
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python server.py
```

Open http://127.0.0.1:5000 in your browser.

On Windows, activate the environment with `.venv\\Scripts\\activate`.

## Configure the Watson endpoint

The app reads the endpoint from `WATSON_EMOTION_URL`. The default is the IBM Skills Network emotion prediction endpoint used in some course labs. If your course provides a different URL or required headers, set the environment variable and update the request headers/payload in `emotion_detection/emotion_detection.py` to match the lab instructions.

macOS/Linux:

```bash
export WATSON_EMOTION_URL="https://your-course-endpoint"
python server.py
```

Do not commit credentials, access tokens, or private endpoints into a public repository. If your course endpoint requires authentication, use environment variables and follow the course's instructions.

## Tests

The unit tests mock the HTTP response so they can test parsing and error handling without depending on the live service.

```bash
python -m unittest -v
```

## Endpoint

`POST /emotionDetector` accepts form data with the key `textToAnalyze`. It returns JSON containing the five emotion scores and `dominant_emotion`. Blank text returns HTTP 400. A service connection or response failure returns HTTP 502.

## Screenshots for course submission

1. Start the app and open it in a browser.
2. Submit a sentence and capture the result if the configured service responds successfully.
3. Submit whitespace-only input and capture the validation message.
4. Save the screenshots locally using the filenames required by your course grader.

Capture screenshots from your own running app; this repository does not claim that the live endpoint has been verified.
