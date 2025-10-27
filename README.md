# GAIA External Brain
Minimal deployment-ready starter for the GAIA External Brain service.

## What is included
- FastAPI app with async SQLAlchemy, APScheduler, Redis placeholder and WebSocket endpoint
- Dockerfile and docker-compose.yml (Postgres + Redis + FastAPI)
- Basic app structure with example routes and placeholders
- requirements.txt and .env.example
- README with run instructions

## Local (Docker Compose)
1. Copy `.env.example` to `.env` and edit values if needed.
2. Build and run:
   ```bash
   docker compose up --build
   ```
3. The API will be available at `http://localhost:8000`.
   - Health: `GET /health`
   - Status: `GET /status`
   - WebSocket: `ws://localhost:8000/ws`

## Railway / Cloud notes
- Railway supports deploying from Dockerfile or from repo. Set environment variables based on `.env.example`.
- Ensure `DATABASE_URL` points to a managed Postgres instance and `REDIS_URL` to a Redis instance.

## Development
- To run locally without Docker:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```

## Structure
```
gaia-external-brain/
├─ app/
│  ├─ main.py
│  ├─ core/
│  ├─ engines/
│  ├─ models/
│  ├─ schemas/
│  └─ services/
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ .env.example
└─ README.md
```

