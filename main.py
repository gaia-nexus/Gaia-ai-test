import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("gaia")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://gaia:gaia@localhost/gaia_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

scheduler = AsyncIOScheduler()

app = FastAPI(title="GAIA External Brain", lifespan=lambda: lifespan_context())

# Simple WebSocket manager
class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

ws_manager = WebSocketManager()

async def sample_scheduled_job():
    logger.info("Running sample scheduled job")
    # Placeholder: add real work here

@asynccontextmanager
async def lifespan_context():
    logger.info("Starting GAIA External Brain (lifespan start)")
    # Create DB tables if models present (placeholder)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    scheduler.add_job(sample_scheduled_job, CronTrigger(second='*/30'), id='sample_job', replace_existing=True)
    scheduler.start()
    try:
        yield
    finally:
        logger.info("Shutting down GAIA External Brain (lifespan end)")
        scheduler.shutdown(wait=False)
        await engine.dispose()

# Middlewares / routes
@app.get("/health")
async def health():
    return JSONResponse({"status": "ok", "env": os.getenv("APP_ENV", "development")})

@app.get("/status")
async def status():
    return JSONResponse({"service": "gaia-external-brain", "uptime": "placeholder"})

@app.get("/api/v1/system/status")
async def system_status():
    return {"status": "operational"}

@app.post("/api/v1/system/heartbeat")
async def heartbeat():
    # placeholder implementation
    return {"heartbeat": "received"}

@app.post("/api/v1/system/orchestrate")
async def orchestrate():
    # placeholder implementation
    return {"orchestrate": "started"}

@app.get("/api/v1/tools")
async def list_tools():
    return {"tools": []}

@app.post("/api/v1/tools/build")
async def build_tool():
    return {"build": "started"}

@app.get("/api/v1/learning/concepts")
async def learning_concepts():
    return {"concepts": []}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back with prefix
            await ws_manager.broadcast(f"echo: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

