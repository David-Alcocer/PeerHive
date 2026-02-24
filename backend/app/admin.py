from fastapi import APIRouter, HTTPException, Request
from typing import List
from bson import ObjectId
from .models import User, RoleEnum

router = APIRouter(prefix="/admin", tags=["Admin"])

# [cite_start]R - READ: Listar usuarios con Kardex pendiente de revisión [cite: 51]
@router.get("/users/pending")
async def get_pending_verifications(request: Request):
    # Usamos la conexión a Mongo que Samuel definió en main.py
    query = {"kardex_screenshot_url": {"$ne": None}, "is_verified": False}
    cursor = request.app.mongodb["users"].find(query)
    users = await cursor.to_list(length=100)
    return users

# [cite_start]U - UPDATE: Promover a Tutor (Asesor) tras revisar el SICEI [cite: 59, 62]
@router.patch("/users/{user_id}/promote")
async def promote_to_advisor(user_id: str, request: Request):
    # 1. Buscar al alumno
    user = await request.app.mongodb["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # [cite_start]2. Validar que tenga el Kardex [cite: 4]
    if not user.get("kardex_screenshot_url"):
        raise HTTPException(status_code=400, detail="Falta evidencia de Kardex")

    # [cite_start]3. Actualizar rol a 'advisor' y marcar como verificado [cite: 62]
    await request.app.mongodb["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": "advisor", "is_verified": True}}
    )
    return {"message": "El estudiante ha sido promovido a Asesor exitosamente"}