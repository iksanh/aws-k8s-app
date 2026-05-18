# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is a **learning project** for CI/CD with FastAPI. The goal is to understand the workflow, not maximize complexity — work through stages in order and don't skip ahead.

## Tech Stack

- Python 3.11+, FastAPI, Uvicorn (ASGI server)
- pytest + httpx (testing)
- ruff (linter & formatter)
- Jenkins (CI/CD) — declarative pipeline in `Jenkinsfile`
- Docker (image build runs in the pipeline)
- Self-managed Kubernetes (lab cluster — deployment target for Stage 7)

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload

# Test
pytest -v

# Lint & format
ruff check .
ruff format .
```

## Project Structure (Intended)

```
app/
  __init__.py
  main.py          # FastAPI entry point
  routes/          # endpoints split per module
tests/
  __init__.py
  test_main.py
Jenkinsfile        # declarative CI pipeline
Dockerfile         # image build (used by Jenkins "Build Image" stage)
.dockerignore
requirements.txt
k8s/               # Kubernetes manifests (Stage 7 — not yet)
```

## Code Conventions

- Use **type hints** on all functions (FastAPI requires them for automatic validation).
- Every new endpoint needs at least 1 happy-path test + 1 error-case test.
- Run `ruff check . && ruff format .` before committing.
- Commit messages follow **conventional commits**: `feat:`, `fix:`, `test:`, `ci:`, `docs:`, `refactor:`.

## CI Pipeline Structure (`Jenkinsfile`)

Declarative pipeline, stages run sequentially; fail the build if any stage is red:
1. Setup Python → Install Dependencies (fresh venv) → Lint (`ruff check .`) → Test (`pytest`) → Build Image (`docker build`)

The Jenkins agent must have `docker` available and the Jenkins user must be in the `docker` group for the Build Image stage to succeed.

## Learning Stages (Roadmap)

- [x] Stage 1 — `GET /health` returning `{"status": "ok"}`
- [x] Stage 2 — First test for `/health` using `TestClient`
- [x] Stage 3 — Setup `ruff`, ensure clean code
- [x] Stage 4 — `Jenkinsfile` running lint + test on Jenkins 
- [x] Stage 5 — Simple CRUD endpoint (in-memory, no database yet)
- [x] Stage 6 — Dockerfile + image build workflow
- [ ] Stage 7 — Deploy to self-managed Kubernetes lab cluster (deferred — user will start later)

## How to Help

This is a learning project — follow this approach when assisting:

- **Explain the concept briefly before giving code.**
- **Don't skip stages.** If the user is on Stage 2, don't hand them a Stage 4 solution.
- **Explain why, not just what** (e.g., why `TestClient` over a real HTTP request).
- Point out **common mistakes** at the current stage.
- If multiple approaches exist, mention them briefly then recommend the most beginner-friendly one.
