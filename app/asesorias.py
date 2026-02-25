from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

router = APIRouter(prefix="/api/asesorias", tags=["Asesorías"])

# Modelo bonito para Swagger
class Asesoria(BaseModel):
    id: int = Field(..., example=1)
    materia: str = Field(..., example="Estructuras de Datos")
    asesor: str = Field(..., example="Freddie Uitzil")
    disponible: bool = Field(..., example=True)

# Fake DB temporal
fake_db: List[Asesoria] = []

@router.get("/", response_model=List[Asesoria], summary="Obtener todas las asesorías")
def get_asesorias():
    return fake_db

@router.post("/", response_model=Asesoria, summary="Crear nueva asesoría")
def create_asesoria(asesoria: Asesoria):
    fake_db.append(asesoria)
    return asesoria

@router.delete("/{asesoria_id}", summary="Eliminar asesoría")
def delete_asesoria(asesoria_id: int):
    for a in fake_db:
        if a.id == asesoria_id:
            fake_db.remove(a)
            return {"message": "Asesoría eliminada"}
    raise HTTPException(status_code=404, detail="Asesoría no encontrada")