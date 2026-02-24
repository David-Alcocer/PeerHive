from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
import os
from . import admin

# Configuration
class Settings(BaseSettings):
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://mongo:27017")
    DB_NAME: str = os.getenv("DB_NAME", "peerhive")

settings = Settings()

# App Initialization
app = FastAPI(title="PeerHive API", version="1.0.0")
app.include_router(admin.router)

# DBase Connection
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    print(f"Connected to MongoDB at {settings.MONGO_URL}")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    print("MongoDB connection closed")

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*" # For dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to PeerHive API"}

@app.get("/health")
async def health():
    return {"status": "ok", "db": "connected" if app.mongodb else "disconnected"}
