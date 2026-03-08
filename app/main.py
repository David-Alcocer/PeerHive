import os
from fastapi import FastAPI, Depends, HTTPException, status, Header
from typing import List, Optional
from dotenv import load_dotenv

# load .env early so db settings pick it up
load_dotenv()

from app import schemas, crud
from bson import ObjectId


app = FastAPI(title="PeerHive - Usuarios CRUD", version="0.1.0")


async def get_current_role(x_role: Optional[str] = Header(None)) -> str:
    # placeholder for authentication/role extraction
    if x_role:
        return x_role.lower()
    return "usuario"


def validate_admin(role: str = Depends(get_current_role)):
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")


@app.post("/api/usuarios", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate):
    created = await crud.create_user(user)
    return schemas.UserResponse(
        id=str(created["_id"]),
        email=created["email"],
        nombre=created["nombre"],
        rol=created["rol"],
    )


@app.get("/api/usuarios", response_model=List[schemas.UserResponse])
async def read_users(rol: Optional[str] = None, current_role: str = Depends(get_current_role)):
    # any authenticated user can list; maybe filter by rol
    users = await crud.list_users(rol)
    return [
        schemas.UserResponse(id=str(u["_id"],), email=u["email"], nombre=u["nombre"], rol=u["rol"])
        for u in users
    ]


@app.get("/api/usuarios/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: str, current_role: str = Depends(get_current_role)):
    user = await crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return schemas.UserResponse(id=str(user["_id"]), email=user["email"], nombre=user["nombre"], rol=user["rol"])


@app.put("/api/usuarios/{user_id}", response_model=schemas.UserResponse, dependencies=[Depends(validate_admin)])
async def update_user(user_id: str, user: schemas.UserUpdate):
    updated = await crud.update_user(user_id, user)
    return schemas.UserResponse(id=str(updated["_id"]), email=updated["email"], nombre=updated["nombre"], rol=updated["rol"])


@app.delete("/api/usuarios/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(validate_admin)])
async def delete_user(user_id: str):
    await crud.delete_user(user_id)
    return None
