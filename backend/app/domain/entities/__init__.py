"""
Entidades del dominio para PeerHive.

Estas clases representan las entidades core del negocio,
independientes de cualquier framework o tecnología de persistencia.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from uuid import UUID, uuid4


class RoleEnum(str, Enum):
    """Roles de usuario en el sistema."""

    ADMIN = "admin"
    ADVISOR = "advisor"
    STUDENT = "student"


class RequestStatusEnum(str, Enum):
    """Estados de una solicitud de asesoría."""

    PENDING = "pending"
    TAKEN = "taken"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MeetingPlatformEnum(str, Enum):
    """Plataformas de reunión."""

    TEAMS = "teams"
    ZOOM = "zoom"
    PRESENCIAL = "presencial"


class SessionStatusEnum(str, Enum):
    """Estados de una sesión."""

    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REQUIRES_REVIEW = "requires_review"
    CANCELLED = "cancelled"


class EvidenceTypeEnum(str, Enum):
    """Tipos de evidencia de asistencia."""

    TEAMS_API = "teams_api"
    MANUAL_UPLOAD = "manual_upload"
    ADMIN_OVERRIDE = "admin_override"


# ── Entidades del Dominio ────────────────────────────────────────────


@dataclass
class AttendanceRecord:
    """Registro de asistencia a una sesión."""

    user_id: str
    joined_at: datetime
    left_at: datetime
    duration_minutes: int


@dataclass
class Verification:
    """Verificación de asistencia a una sesión."""

    was_held: bool
    attendance: List[AttendanceRecord] = field(default_factory=list)
    duration_minutes: Optional[int] = None
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    evidence_type: EvidenceTypeEnum = EvidenceTypeEnum.TEAMS_API
    manual_evidence: Optional[Dict[str, Any]] = None
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    notes: Optional[str] = None


@dataclass
class Attachment:
    """Archivo adjunto en un mensaje."""

    type: str  # image, document
    url: str
    name: str


@dataclass
class Message:
    """Mensaje en un chat."""

    from_user_id: str
    content: Optional[str] = None
    attachment: Optional[Attachment] = None
    sent_at: datetime = field(default_factory=datetime.now)
    is_read: bool = False


@dataclass
class User:
    """
    Entidad de Usuario del dominio.

    Representa un usuario del sistema PeerHive.
    """

    id: Optional[str] = None
    name: str = ""
    email: str = ""
    microsoft_id: str = ""
    role: RoleEnum = RoleEnum.STUDENT
    advisor_subjects: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Campos adicionales para autenticación (no persistidos en dominio)
    password_hash: Optional[str] = None

    def is_advisor(self) -> bool:
        return self.role == RoleEnum.ADVISOR

    def is_admin(self) -> bool:
        return self.role == RoleEnum.ADMIN

    def is_student(self) -> bool:
        return self.role == RoleEnum.STUDENT


@dataclass
class Subject:
    """Entidad de Materia del dominio."""

    id: Optional[str] = None
    name: str = ""
    description: Optional[str] = None
    is_active: bool = True
    created_by: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Request:
    """
    Entidad de Solicitud del dominio.

    Representa una solicitud de asesoría realizada por un estudiante.
    """

    id: Optional[str] = None
    student_id: str = ""
    advisor_id: Optional[str] = None
    subject: str = ""
    topic: str = ""
    description: Optional[str] = None
    status: RequestStatusEnum = RequestStatusEnum.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    taken_at: Optional[datetime] = None

    def is_pending(self) -> bool:
        return self.status == RequestStatusEnum.PENDING

    def is_taken(self) -> bool:
        return self.status == RequestStatusEnum.TAKEN

    def is_completed(self) -> bool:
        return self.status == RequestStatusEnum.COMPLETED


@dataclass
class Session:
    """
    Entidad de Sesión del dominio.

    Representa una sesión de asesoría programada.
    """

    id: Optional[str] = None
    request_id: str = ""
    student_id: str = ""
    advisor_id: str = ""
    approved_by: Optional[str] = None

    scheduled_at: datetime = field(default_factory=datetime.now)
    meeting_platform: MeetingPlatformEnum = MeetingPlatformEnum.TEAMS
    meeting_link: Optional[str] = None
    teams_meeting_id: Optional[str] = None

    status: SessionStatusEnum = SessionStatusEnum.PENDING_APPROVAL

    verification: Optional[Verification] = None

    created_at: datetime = field(default_factory=datetime.now)
    approved_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def is_pending(self) -> bool:
        return self.status == SessionStatusEnum.PENDING_APPROVAL

    def is_approved(self) -> bool:
        return self.status == SessionStatusEnum.APPROVED

    def is_completed(self) -> bool:
        return self.status == SessionStatusEnum.COMPLETED


@dataclass
class Chat:
    """Entidad de Chat del dominio."""

    id: Optional[str] = None
    session_id: str = ""
    student_id: str = ""
    advisor_id: str = ""
    messages: List[Message] = field(default_factory=list)
    last_message_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
