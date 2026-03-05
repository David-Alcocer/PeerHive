"""
Capa de Dominio de PeerHive.

Contiene las entidades del negocio y los puertos (interfaces)
que definen los contratos para la infraestructura.
"""
from .entities import (
    User,
    Request,
    Session,
    Subject,
    Chat,
    Message,
    Attachment,
    Verification,
    AttendanceRecord,
    RoleEnum,
    RequestStatusEnum,
    MeetingPlatformEnum,
    SessionStatusEnum,
    EvidenceTypeEnum
)

from .repositories import (
    UserRepositoryPort,
    RequestRepositoryPort,
    SessionRepositoryPort,
    SubjectRepositoryPort,
    ChatRepositoryPort
)

__all__ = [
    # Entities
    "User",
    "Request",
    "Session",
    "Subject",
    "Chat",
    "Message",
    "Attachment",
    "Verification",
    "AttendanceRecord",
    "RoleEnum",
    "RequestStatusEnum",
    "MeetingPlatformEnum",
    "SessionStatusEnum",
    "EvidenceTypeEnum",
    # Ports
    "UserRepositoryPort",
    "RequestRepositoryPort",
    "SessionRepositoryPort",
    "SubjectRepositoryPort",
    "ChatRepositoryPort"
]
