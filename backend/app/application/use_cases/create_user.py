"""
Caso de uso: Crear Usuario.

Crea un nuevo usuario en el sistema.
"""
from typing import Optional
from datetime import datetime

from ...domain.entities import User, RoleEnum
from ...domain.repositories import UserRepositoryPort


class CreateUserUseCase:
    """
    Caso de uso para crear un nuevo usuario.
    """
    
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository
    
    async def execute(
        self,
        name: str,
        email: str,
        password_hash: str,
        role: str = "student",
        microsoft_id: str = "",
        advisor_subjects: Optional[list] = None
    ) -> User:
        """
        Ejecuta el caso de uso para crear un usuario.
        
        Args:
            name: Nombre del usuario
            email: Correo electrónico del usuario
            password_hash: Hash de la contraseña
            role: Rol del usuario (student, advisor, admin)
            microsoft_id: ID de Microsoft (opcional)
            advisor_subjects: Lista de materias que puede enseñar (solo para asesores)
            
        Returns:
            El usuario creado
            
        Raises:
            ValueError: Si el correo ya está registrado
        """
        # Verificar si el usuario ya existe
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("El correo ya está registrado")
        
        # Crear la entidad de dominio
        user = User(
            name=name,
            email=email,
            microsoft_id=microsoft_id,
            role=RoleEnum(role),
            advisor_subjects=advisor_subjects or [],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            password_hash=password_hash
        )
        
        # Persistir el usuario
        created_user = await self.user_repository.create(user)
        
        return created_user
