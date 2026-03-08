from typing import List, Optional
from app import schemas, db
from passlib.context import CryptContext
from bson import ObjectId
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(email: str) -> Optional[dict]:
    return await db.users_collection.find_one({"email": email})


async def get_user(id: str) -> Optional[dict]:
    if not ObjectId.is_valid(id):
        return None
    return await db.users_collection.find_one({"_id": ObjectId(id)})


async def list_users(role: Optional[str] = None) -> List[dict]:
    query = {}
    if role:
        query["rol"] = role.lower()
    cursor = db.users_collection.find(query)
    return [user async for user in cursor]


def _validate_institutional_email(email: str) -> bool:
    # simple check: must end with an institutional domain (e.g. '@universidad.edu')
    # adjust pattern as needed or pull from config
    return email.lower().endswith(".edu") or email.lower().endswith("@university.com")


def _validate_password_strength(password: str) -> bool:
    # basic rules: at least 8 chars, contains number and letter
    import re
    return len(password) >= 8 and re.search(r"[0-9]", password) and re.search(r"[A-Za-z]", password)


async def create_user(user_in: schemas.UserCreate) -> dict:
    # institutional email check
    if not _validate_institutional_email(user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must be institutional")

    # password strength
    if not _validate_password_strength(user_in.contraseña):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password does not meet security requirements")

    # email uniqueness
    existing = await get_user_by_email(user_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = pwd_context.hash(user_in.contraseña)
    doc = {
        "email": user_in.email,
        "nombre": user_in.nombre,
        "contraseña": hashed_password,
        "rol": user_in.rol.lower(),
    }
    result = await db.users_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


async def update_user(id: str, user_in: schemas.UserUpdate) -> dict:
    current = await get_user(id)
    if not current:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = {}
    if user_in.email and user_in.email != current.get("email"):
        # check institutional pattern
        if not _validate_institutional_email(user_in.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must be institutional")
        # ensure not duplicated
        exists = await get_user_by_email(user_in.email)
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        update_data["email"] = user_in.email
    if user_in.nombre:
        update_data["nombre"] = user_in.nombre
    if user_in.rol:
        update_data["rol"] = user_in.rol.lower()

    if update_data:
        await db.users_collection.update_one({"_id": current["_id"]}, {"$set": update_data})
        current.update(update_data)
    return current


async def delete_user(id: str) -> None:
    user = await get_user(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # TODO: check for related data constraints maybe by external services
    await db.users_collection.delete_one({"_id": user["_id"]})
