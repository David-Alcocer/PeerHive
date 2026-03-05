"""
Repositorio de Sesiones para MongoDB.

Implementación del puerto SessionRepositoryPort usando MongoDB.
"""
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from ...domain.entities import Session, SessionStatusEnum, MeetingPlatformEnum, Verification, EvidenceTypeEnum
from ...domain.repositories import SessionRepositoryPort


class SessionRepository(SessionRepositoryPort):
    """
    Implementación del repositorio de sesiones para MongoDB.
    """
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.sessions
    
    def _to_entity(self, doc: dict) -> Optional[Session]:
        """Convierte un documento MongoDB a entidad de dominio."""
        if not doc:
            return None
        
        # Convertir verification si existe
        verification = None
        if doc.get("verification"):
            v = doc["verification"]
            verification = Verification(
                was_held=v.get("wasHeld", False),
                duration_minutes=v.get("durationMinutes"),
                actual_start_time=v.get("actualStartTime"),
                actual_end_time=v.get("actualEndTime"),
                evidence_type=EvidenceTypeEnum(v.get("evidenceType", "teams_api")),
                manual_evidence=v.get("manualEvidence"),
                verified_by=str(v.get("verifiedBy")) if v.get("verifiedBy") else None,
                verified_at=v.get("verifiedAt"),
                notes=v.get("notes")
            )
        
        return Session(
            id=str(doc.get("_id", "")),
            request_id=str(doc.get("requestId", "")),
            student_id=str(doc.get("studentId", "")),
            advisor_id=str(doc.get("advisorId", "")),
            approved_by=str(doc.get("approvedBy")) if doc.get("approvedBy") else None,
            scheduled_at=doc.get("scheduledAt", datetime.now()),
            meeting_platform=MeetingPlatformEnum(doc.get("meetingPlatform", "teams")),
            meeting_link=doc.get("meetingLink"),
            teams_meeting_id=doc.get("teamsMeetingId"),
            status=SessionStatusEnum(doc.get("status", "pending_approval")),
            verification=verification,
            created_at=doc.get("createdAt", datetime.now()),
            approved_at=doc.get("approvedAt"),
            completed_at=doc.get("completedAt")
        )
    
    def _to_document(self, session: Session) -> dict:
        """Convierte una entidad de dominio a documento MongoDB."""
        doc = {
            "requestId": ObjectId(session.request_id),
            "studentId": ObjectId(session.student_id),
            "advisorId": ObjectId(session.advisor_id),
            "scheduledAt": session.scheduled_at,
            "meetingPlatform": session.meeting_platform.value,
            "status": session.status.value
        }
        
        if session.approved_by:
            doc["approvedBy"] = ObjectId(session.approved_by)
        
        if session.meeting_link:
            doc["meetingLink"] = session.meeting_link
        
        if session.teams_meeting_id:
            doc["teamsMeetingId"] = session.teams_meeting_id
        
        if session.verification:
            v = session.verification
            doc["verification"] = {
                "wasHeld": v.was_held,
                "durationMinutes": v.duration_minutes,
                "actualStartTime": v.actual_start_time,
                "actualEndTime": v.actual_end_time,
                "evidenceType": v.evidence_type.value,
                "manualEvidence": v.manual_evidence,
                "verifiedBy": ObjectId(v.verified_by) if v.verified_by else None,
                "verifiedAt": v.verified_at,
                "notes": v.notes
            }
        
        if session.id:
            doc["_id"] = ObjectId(session.id)
        else:
            doc["createdAt"] = session.created_at
        
        if session.approved_at:
            doc["approvedAt"] = session.approved_at
        
        if session.completed_at:
            doc["completedAt"] = session.completed_at
        
        return doc
    
    async def create(self, session: Session) -> Session:
        """Crea una nueva sesión."""
        doc = self._to_document(session)
        doc["createdAt"] = datetime.now()
        
        result = await self.collection.insert_one(doc)
        session.id = str(result.inserted_id)
        return session
    
    async def get_by_id(self, session_id: str) -> Optional[Session]:
        """Obtiene una sesión por su ID."""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(session_id)})
            return self._to_entity(doc)
        except Exception:
            return None
    
    async def get_by_request_id(self, request_id: str) -> Optional[Session]:
        """Obtiene una sesión por ID de solicitud."""
        try:
            doc = await self.collection.find_one({"requestId": ObjectId(request_id)})
            return self._to_entity(doc)
        except Exception:
            return None
    
    async def update(self, session: Session) -> Session:
        """Actualiza una sesión existente."""
        doc = self._to_document(session)
        
        await self.collection.replace_one(
            {"_id": ObjectId(session.id)},
            doc
        )
        return session
    
    async def delete(self, session_id: str) -> bool:
        """Elimina una sesión por su ID."""
        result = await self.collection.delete_one({"_id": ObjectId(session_id)})
        return result.deleted_count > 0
    
    async def list_all(self) -> List[Session]:
        """Lista todas las sesiones."""
        cursor = self.collection.find()
        return [self._to_entity(doc) async for doc in cursor]
    
    async def list_by_student(self, student_id: str) -> List[Session]:
        """Lista sesiones de un estudiante."""
        cursor = self.collection.find({"studentId": ObjectId(student_id)})
        return [self._to_entity(doc) async for doc in cursor]
    
    async def list_by_advisor(self, advisor_id: str) -> List[Session]:
        """Lista sesiones de un asesor."""
        cursor = self.collection.find({"advisorId": ObjectId(advisor_id)})
        return [self._to_entity(doc) async for doc in cursor]
    
    async def list_by_status(self, status: SessionStatusEnum) -> List[Session]:
        """Lista sesiones por estado."""
        cursor = self.collection.find({"status": status.value})
        return [self._to_entity(doc) async for doc in cursor]
    
    async def approve_session(self, session_id: str, approved_by: str) -> Session:
        """Aprueba una sesión."""
        now = datetime.now()
        await self.collection.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$set": {
                    "approvedBy": ObjectId(approved_by),
                    "status": SessionStatusEnum.APPROVED.value,
                    "approvedAt": now
                }
            }
        )
        
        session = await self.get_by_id(session_id)
        return session
    
    async def complete_session(self, session_id: str) -> Session:
        """Completa una sesión."""
        now = datetime.now()
        await self.collection.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$set": {
                    "status": SessionStatusEnum.COMPLETED.value,
                    "completedAt": now
                }
            }
        )
        
        session = await self.get_by_id(session_id)
        return session
