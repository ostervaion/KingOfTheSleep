import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from controllers import router as controllers_router
from core.config import AVATAR_DIR, ORIGINS
from core.database import create_db_and_tables
from schedules.battle_scheduler import battle_scheduler
from sockets.ws import websocket_endpoint


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
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

app.include_router(controllers_router)
app.websocket("/ws")(websocket_endpoint)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
def health():
    return {"status": "ok"}
