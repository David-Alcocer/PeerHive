"""
Contenedor de Inyección de Dependencias de PeerHive.

Proporciona las instancias de repositorios y casos de uso
para la aplicación.
"""
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..domain.repositories import (
    UserRepositoryPort,
    RequestRepositoryPort,
    SessionRepositoryPort
)
from ..infrastructure.repositories import (
    UserRepository,
    RequestRepository,
    SessionRepository
)
from ..application.use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    CreateRequestUseCase,
    AssignRequestUseCase
)


class Container:
    """
    Contenedor de inyección de dependencias.
    
    Proporciona acceso a los repositorios y casos de uso
    de la aplicación.
    """
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self._database = database
        self._user_repository = None
        self._request_repository = None
        self._session_repository = None
    
    @property
    def user_repository(self) -> UserRepositoryPort:
        """Obtiene el repositorio de usuarios."""
        if self._user_repository is None:
            self._user_repository = UserRepository(self._database)
        return self._user_repository
    
    @property
    def request_repository(self) -> RequestRepositoryPort:
        """Obtiene el repositorio de solicitudes."""
        if self._request_repository is None:
            self._request_repository = RequestRepository(self._database)
        return self._request_repository
    
    @property
    def session_repository(self) -> SessionRepositoryPort:
        """Obtiene el repositorio de sesiones."""
        if self._session_repository is None:
            self._session_repository = SessionRepository(self._database)
        return self._session_repository
    
    @property
    def create_user_use_case(self) -> CreateUserUseCase:
        """Obtiene el caso de uso de crear usuario."""
        return CreateUserUseCase(self.user_repository)
    
    @property
    def get_user_use_case(self) -> GetUserUseCase:
        """Obtiene el caso de uso de obtener usuario."""
        return GetUserUseCase(self.user_repository)
    
    @property
    def create_request_use_case(self) -> CreateRequestUseCase:
        """Obtiene el caso de uso de crear solicitud."""
        return CreateRequestUseCase(self.request_repository)
    
    @property
    def assign_request_use_case(self) -> AssignRequestUseCase:
        """Obtiene el caso de uso de asignar solicitud."""
        return AssignRequestUseCase(self.request_repository)


# Instancia global del contenedor (se inicializa en startup)
_container: Container = None


def get_container() -> Container:
    """Obtiene la instancia global del contenedor."""
    global _container
    return _container


def init_container(database: AsyncIOMotorDatabase):
    """Inicializa el contenedor con la base de datos."""
    global _container
    _container = Container(database)
