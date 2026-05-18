# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is a **learning project** for CI/CD with FastAPI. The goal is to understand the workflow, not maximize complexity — work through stages in order and don't skip ahead.

## Tech Stack

- Python 3.11+, FastAPI, Uvicorn (ASGI server)
- pytest + httpx (testing)
- ruff (linter & formatter)
- GitHub Actions (CI/CD)
- Docker (optional, later stages)

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
.github/workflows/ci.yml
requirements.txt
Dockerfile         # optional
```

## Code Conventions

- Use **type hints** on all functions (FastAPI requires them for automatic validation).
- Every new endpoint needs at least 1 happy-path test + 1 error-case test.
- Run `ruff check . && ruff format .` before committing.
- Commit messages follow **conventional commits**: `feat:`, `fix:`, `test:`, `ci:`, `docs:`, `refactor:`.

## CI Pipeline Structure (`.github/workflows/ci.yml`)

Run sequentially; fail the PR if any step is red:
1. Checkout → Setup Python → `pip install -r requirements.txt` → `ruff check .` → `pytest`

Trigger on `push` to `main` and all `pull_request` events.

## Learning Stages (Roadmap)

- [ ] Stage 1 — `GET /health` returning `{"status": "ok"}`
- [ ] Stage 2 — First test for `/health` using `TestClient`
- [ ] Stage 3 — Setup `ruff`, ensure clean code
- [ ] Stage 4 — `ci.yml` running lint + test on GitHub Actions
- [ ] Stage 5 — Simple CRUD endpoint (in-memory, no database yet)
- [ ] Stage 6 — Dockerfile + image build workflow
- [ ] Stage 7 — Auto-deploy to Railway / Fly.io / Render

## How to Help

This is a learning project — follow this approach when assisting:

- **Explain the concept briefly before giving code.**
- **Don't skip stages.** If the user is on Stage 2, don't hand them a Stage 4 solution.
- **Explain why, not just what** (e.g., why `TestClient` over a real HTTP request).
- Point out **common mistakes** at the current stage.
- If multiple approaches exist, mention them briefly then recommend the most beginner-friendly one.
