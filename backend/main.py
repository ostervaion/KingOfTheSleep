from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import ORIGINS
from database import create_db_and_tables
from routes import router
from ws import websocket_endpoint

app = FastAPI(title="King of the Sleep API")
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
