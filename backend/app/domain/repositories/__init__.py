"""
Puertos (interfaces) del dominio para PeerHive.

Estos puertos definen los contratos que deben implementar
los adaptadores de infraestructura (repositorios).
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from ..entities import (
    User,
    Request,
    Session,
    Subject,
    Chat,
    RoleEnum,
    RequestStatusEnum,
    SessionStatusEnum,
)

# ── Puerto de Usuario ────────────────────────────────────────────────


class UserRepositoryPort(ABC):
    """
    Puerto para el repositorio de usuarios.

    Define la interfaz que debe implementar cualquier adapter
    que persista usuarios (MongoDB, SQL, etc.).
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """Crea un nuevo usuario."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su correo electrónico."""
        pass

    @abstractmethod
    async def get_by_microsoft_id(self, microsoft_id: str) -> Optional[User]:
        """Obtiene un usuario por su ID de Microsoft."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Actualiza un usuario existente."""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Elimina un usuario por su ID."""
        pass

    @abstractmethod
    async def list_all(self) -> List[User]:
        """Lista todos los usuarios."""
        pass

    @abstractmethod
    async def list_by_role(self, role: RoleEnum) -> List[User]:
        """Lista usuarios por rol."""
        pass

    @abstractmethod
    async def list_advisors_by_subject(self, subject: str) -> List[User]:
        """Lista asesores que pueden enseñar una materia."""
        pass


# ── Puerto de Solicitud ────────────────────────────────────────────────


class RequestRepositoryPort(ABC):
    """
    Puerto para el repositorio de solicitudes.

    Define la interfaz para persistir solicitudes de asesoría.
    """

    @abstractmethod
    async def create(self, request: Request) -> Request:
        """Crea una nueva solicitud."""
        pass

    @abstractmethod
    async def get_by_id(self, request_id: str) -> Optional[Request]:
        """Obtiene una solicitud por su ID."""
        pass

    @abstractmethod
    async def update(self, request: Request) -> Request:
        """Actualiza una solicitud existente."""
        pass

    @abstractmethod
    async def delete(self, request_id: str) -> bool:
        """Elimina una solicitud por su ID."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Request]:
        """Lista todas las solicitudes."""
        pass

    @abstractmethod
    async def list_pending(self) -> List[Request]:
        """Lista todas las solicitudes pendientes."""
        pass

    @abstractmethod
    async def list_by_student(self, student_id: str) -> List[Request]:
        """Lista solicitudes de un estudiante."""
        pass

    @abstractmethod
    async def list_by_advisor(self, advisor_id: str) -> List[Request]:
        """Lista solicitudes asignadas a un asesor."""
        pass

    @abstractmethod
    async def list_by_status(self, status: RequestStatusEnum) -> List[Request]:
        """Lista solicitudes por estado."""
        pass

    @abstractmethod
    async def assign_to_advisor(self, request_id: str, advisor_id: str) -> Request:
        """Asigna una solicitud a un asesor."""
        pass


# ── Puerto de Sesión ──────────────────────────────────────────────────


class SessionRepositoryPort(ABC):
    """
    Puerto para el repositorio de sesiones.

    Define la interfaz para persistir sesiones de asesoría.
    """

    @abstractmethod
    async def create(self, session: Session) -> Session:
        """Crea una nueva sesión."""
        pass

    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[Session]:
        """Obtiene una sesión por su ID."""
        pass

    @abstractmethod
    async def get_by_request_id(self, request_id: str) -> Optional[Session]:
        """Obtiene una sesión por ID de solicitud."""
        pass

    @abstractmethod
    async def update(self, session: Session) -> Session:
        """Actualiza una sesión existente."""
        pass

    @abstractmethod
    async def delete(self, session_id: str) -> bool:
        """Elimina una sesión por su ID."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Session]:
        """Lista todas las sesiones."""
        pass

    @abstractmethod
    async def list_by_student(self, student_id: str) -> List[Session]:
        """Lista sesiones de un estudiante."""
        pass

    @abstractmethod
    async def list_by_advisor(self, advisor_id: str) -> List[Session]:
        """Lista sesiones de un asesor."""
        pass

    @abstractmethod
    async def list_by_status(self, status: SessionStatusEnum) -> List[Session]:
        """Lista sesiones por estado."""
        pass

    @abstractmethod
    async def approve_session(self, session_id: str, approved_by: str) -> Session:
        """Aprueba una sesión."""
        pass

    @abstractmethod
    async def complete_session(self, session_id: str) -> Session:
        """Completa una sesión."""
        pass


# ── Puerto de Materia ────────────────────────────────────────────────


class SubjectRepositoryPort(ABC):
    """
    Puerto para el repositorio de materias.

    Define la interfaz para persistir materias.
    """

    @abstractmethod
    async def create(self, subject: Subject) -> Subject:
        """Crea una nueva materia."""
        pass

    @abstractmethod
    async def get_by_id(self, subject_id: str) -> Optional[Subject]:
        """Obtiene una materia por su ID."""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Subject]:
        """Obtiene una materia por nombre."""
        pass

    @abstractmethod
    async def update(self, subject: Subject) -> Subject:
        """Actualiza una materia existente."""
        pass

    @abstractmethod
    async def delete(self, subject_id: str) -> bool:
        """Elimina una materia por su ID."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Subject]:
        """Lista todas las materias."""
        pass

    @abstractmethod
    async def list_active(self) -> List[Subject]:
        """Lista las materias activas."""
        pass


# ── Puerto de Chat ───────────────────────────────────────────────────


class ChatRepositoryPort(ABC):
    """
    Puerto para el repositorio de chats.

    Define la interfaz para persistir chats.
    """

    @abstractmethod
    async def create(self, chat: Chat) -> Chat:
        """Crea un nuevo chat."""
        pass

    @abstractmethod
    async def get_by_id(self, chat_id: str) -> Optional[Chat]:
        """Obtiene un chat por su ID."""
        pass

    @abstractmethod
    async def get_by_session_id(self, session_id: str) -> Optional[Chat]:
        """Obtiene un chat por ID de sesión."""
        pass

    @abstractmethod
    async def update(self, chat: Chat) -> Chat:
        """Actualiza un chat existente."""
        pass

    @abstractmethod
    async def delete(self, chat_id: str) -> bool:
        """Elimina un chat por su ID."""
        pass

    @abstractmethod
    async def list_by_user(self, user_id: str) -> List[Chat]:
        """Lista chats de un usuario."""
        pass
