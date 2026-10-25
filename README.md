# ci-cd-final-project

IBM CI/CD final project: a Flask-based Emotion Detection application used to demonstrate continuous integration and continuous delivery with GitHub Actions and Tekton.

The application analyzes user-provided text and returns emotion scores and the dominant emotion.

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 server.py
```

## CI workflow

The GitHub Actions workflow installs dependencies, runs flake8 linting, and runs the nose unit-test suite.

## Tekton tasks

The `.tekton/tasks.yml` file defines cleanup, source cloning, linting, unit testing, image building, and OpenShift deployment tasks.

OpenShift screenshots and successful PipelineRun evidence must come from the actual course OpenShift environment.