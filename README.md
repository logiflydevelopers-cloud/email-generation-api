# Email Generator API

FastAPI-based email generation service using OpenAI.

## Endpoints

- GET /health
- POST /api/v1/email/write
- POST /api/v1/email/reply
- POST /api/v1/email/template

## Local Run

```bash
uvicorn app.main:app --reload
