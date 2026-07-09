from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
from pathlib import Path
from config import ORIGINS
from database import create_db_and_tables
from routes import AVATAR_DIR, router
from ws import websocket_endpoint

from contextlib import asynccontextmanager
from fastapi import FastAPI
from battle_scheduler import battle_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables() #after lifespan implementation the startup gets cancelled, the database needs to be here
    task = asyncio.create_task(battle_scheduler())
    yield
    task.cancel()

app = FastAPI(title="King of the Sleep API", lifespan=lifespan)
app.mount("/uploads", StaticFiles(directory=str(AVATAR_DIR.parent)), name="uploads")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
app.websocket("/ws")(websocket_endpoint)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
def health():
    return {"status": "ok"}
