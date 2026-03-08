from motor.motor_asyncio import AsyncIOMotorClient
import os
from functools import lru_cache


class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "peERhIVE")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]

# Collection for users
users_collection = db.get_collection("usuarios")
