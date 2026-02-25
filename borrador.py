from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI(title="Peerhive API - Módulo de Usuarios y Admin")

# --- 1. CONFIGURACIÓN DE BASE DE DATOS (MongoDB) ---
# Sustituye con tu URI de MongoDB
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.peerhive
user_collection = database.get_collection("users")

# --- 2. MODELOS DE DATOS (POO / Pydantic) ---

# Clase para manejar el ID de MongoDB en las respuestas JSON
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v): raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# Molde Único (Atributos de Omar + Tus requerimientos de Admin)
class UserBase(BaseModel):
    full_name: str
    [cite_start]email: EmailStr # Validado automáticamente [cite: 14]
    [cite_start]role: str = "student" # Valores: admin, student, tutor [cite: 8]
    is_verified: bool = False # Estado inicial
    career: Optional[str] = None
    semester: Optional[int] = None
    id_card_url: Optional[str] = None # Link a credencial
    kardex_screenshot_url: Optional[str] = None # Link a captura SICEI

# [cite_start]Lo que Omar recibe para el Registro (CREATE) [cite: 11]
class UserCreate(UserBase):
    [cite_start]password: str # Encriptada en el backend [cite: 8, 15]

# [cite_start]Lo que el sistema devuelve (READ) sin la contraseña [cite: 22, 25]
class UserResponse(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# --- 3. LÓGICA DE SEGURIDAD ---
async def check_admin_auth(admin_id: str):
    """Verifica que el usuario que intenta ejecutar la acción sea Admin"""
    user = await user_collection.find_one({"_id": ObjectId(admin_id)})
    if not user or user.get("role") != "admin":
        [cite_start]raise HTTPException(status_code=403, detail="Solo administradores autorizados [cite: 67]")
    return user

# --- 4. ENDPOINTS DEL CRUD ---

# [cite_start]C - CREATE: Registro inicial (Omar) [cite: 10, 47]
@app.post("/api/usuarios", response_model=UserResponse)
async def create_user(user: UserCreate):
    # [cite_start]Verificar si el mail ya existe [cite: 14]
    existing = await user_collection.find_one({"email": user.email})
    if existing: raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    user_dict = user.dict()
    new_user = await user_collection.insert_one(user_dict)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return created_user

# R - READ: Listar pendientes de verificación (Tú - Admin)
@app.get("/admin/users/pending", response_model=List[UserResponse])
async def get_pending_users(admin_id: str):
    await check_admin_auth(admin_id)
    # Buscamos quienes subieron kardex pero no son tutores aún
    query = {"kardex_screenshot_url": {"$ne": None}, "role": "student"}
    cursor = user_collection.find(query)
    return await cursor.to_list(length=100)

# U - UPDATE: Validar y Promover a Tutor (Tú - Admin)
@app.patch("/admin/users/{user_id}/promote")
async def promote_to_tutor(user_id: str, admin_id: str):
    await check_admin_auth(admin_id)
    
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    [cite_start]if not user: raise HTTPException(status_code=404, detail="Usuario no existe [cite: 33]")
    
    # Validación: Debe existir la captura del Kardex
    if not user.get("kardex_screenshot_url"):
        raise HTTPException(status_code=400, detail="Falta evidencia de Kardex para promover")

    # Actualización parcial (PATCH)
    await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": "tutor", "is_verified": True}}
    )
    [cite_start]return {"message": "Usuario verificado y promovido a Tutor exitosamente [cite: 34]"}

# [cite_start]D - DELETE: Eliminar usuario (Omar/Tú) [cite: 36, 63]
@app.delete("/api/usuarios/{user_id}")
async def delete_user(user_id: str, admin_id: str):
    await check_admin_auth(admin_id)
    delete_result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    if delete_result.deleted_count == 1:
        [cite_start]return {"message": "Usuario eliminado correctamente [cite: 38]"}
    [cite_start]raise HTTPException(status_code=404, detail="Usuario no encontrado [cite: 40]")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)