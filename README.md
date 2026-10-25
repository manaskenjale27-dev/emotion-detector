# Final Project

IBM Applied AI final project: Emotion Detection using the Watson NLP service and a Flask web application.

This application analyzes user-provided text and returns scores for anger, disgust, fear, joy, and sadness, together with the dominant emotion.

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 server.py
```

Open http://127.0.0.1:5000.

## Validation

GitHub Actions runs flake8 linting and the Python unit tests. Tekton task definitions for cleanup and lint/test are in `.tekton/tasks.yml`.

## OpenShift note

OpenShift deployment and pipeline run evidence must be produced in the course's OpenShift cluster. Do not treat this repository file as proof that a pipeline or deployment has already run.
