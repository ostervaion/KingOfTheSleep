from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, time, timedelta
from config import settings
from database import engine, Base
from routers import items

horadestino = time(20, 0, 0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="App API",
    version="1.0.0",
    lifespan=lifespan,
    # Serve docs under /api/docs when behind Caddy
    root_path="/api",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router, prefix="/items", tags=["items"])


@app.get("/nextbattle")
def nextbattle():
    now = datetime.now()
    
    meta = datetime.combine(now.date(), horadestino)
    
    if now >= meta:
        meta += timedelta(days=1)
        
    diferencia = meta - now

    segundos = int(diferencia.total_seconds())
    return {"nextbattle": segundos}

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "API is running"}
