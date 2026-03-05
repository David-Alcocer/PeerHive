"""
Repositorio de Solicitudes para MongoDB.

Implementación del puerto RequestRepositoryPort usando MongoDB.
"""
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from ...domain.entities import Request, RequestStatusEnum
from ...domain.repositories import RequestRepositoryPort


class RequestRepository(RequestRepositoryPort):
    """
    Implementación del repositorio de solicitudes para MongoDB.
    """
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.requests
    
    def _to_entity(self, doc: dict) -> Optional[Request]:
        """Convierte un documento MongoDB a entidad de dominio."""
        if not doc:
            return None
        
        return Request(
            id=str(doc.get("_id", "")),
            student_id=str(doc.get("studentId", "")),
            advisor_id=str(doc.get("advisorId")) if doc.get("advisorId") else None,
            subject=doc.get("subject", ""),
            topic=doc.get("topic", ""),
            description=doc.get("description"),
            status=RequestStatusEnum(doc.get("status", "pending")),
            created_at=doc.get("createdAt", datetime.now()),
            taken_at=doc.get("takenAt")
        )
    
    def _to_document(self, request: Request) -> dict:
        """Convierte una entidad de dominio a documento MongoDB."""
        doc = {
            "studentId": ObjectId(request.student_id),
            "subject": request.subject,
            "topic": request.topic,
            "status": request.status.value
        }
        
        if request.advisor_id:
            doc["advisorId"] = ObjectId(request.advisor_id)
        
        if request.description:
            doc["description"] = request.description
        
        if request.id:
            doc["_id"] = ObjectId(request.id)
        else:
            doc["createdAt"] = request.created_at
        
        if request.taken_at:
            doc["takenAt"] = request.taken_at
        
        return doc
    
    async def create(self, request: Request) -> Request:
        """Crea una nueva solicitud."""
        doc = self._to_document(request)
        doc["createdAt"] = datetime.now()
        
        result = await self.collection.insert_one(doc)
        request.id = str(result.inserted_id)
        return request
    
    async def get_by_id(self, request_id: str) -> Optional[Request]:
        """Obtiene una solicitud por su ID."""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(request_id)})
            return self._to_entity(doc)
        except Exception:
            return None
    
    async def update(self, request: Request) -> Request:
        """Actualiza una solicitud existente."""
        doc = self._to_document(request)
        
        await self.collection.replace_one(
            {"_id": ObjectId(request.id)},
            doc
        )
        return request
    
    async def delete(self, request_id: str) -> bool:
        """Elimina una solicitud por su ID."""
        result = await self.collection.delete_one({"_id": ObjectId(request_id)})
        return result.deleted_count > 0
    
    async def list_all(self) -> List[Request]:
        """Lista todas las solicitudes."""
        cursor = self.collection.find()
        return [self._to_entity(doc) async for doc in cursor]
    
    async def list_pending(self) -> List[Request]:
        """Lista todas las solicitudes pendientes."""
        cursor = self.collection.find({"status": RequestStatusEnum.PENDING.value})
        return [self._to_entity(doc) async for doc in cursor]
    
    async def list_by_student(self, student_id: str) -> List[Request]:
        """Lista solicitudes de un estudiante."""
        cursor = self.collection.find({"studentId": ObjectId(student_id)})
        return [self._to_entity(doc) async for doc in cursor]
    
    async def list_by_advisor(self, advisor_id: str) -> List[Request]:
        """Lista solicitudes asignadas a un asesor."""
        cursor = self.collection.find({"advisorId": ObjectId(advisor_id)})
        return [self._to_entity(doc) async for doc in cursor]
    
    async def list_by_status(self, status: RequestStatusEnum) -> List[Request]:
        """Lista solicitudes por estado."""
        cursor = self.collection.find({"status": status.value})
        return [self._to_entity(doc) async for doc in cursor]
    
    async def assign_to_advisor(self, request_id: str, advisor_id: str) -> Request:
        """Asigna una solicitud a un asesor."""
        now = datetime.now()
        await self.collection.update_one(
            {"_id": ObjectId(request_id)},
            {
                "$set": {
                    "advisorId": ObjectId(advisor_id),
                    "status": RequestStatusEnum.TAKEN.value,
                    "takenAt": now
                }
            }
        )
        
        request = await self.get_by_id(request_id)
        return request
