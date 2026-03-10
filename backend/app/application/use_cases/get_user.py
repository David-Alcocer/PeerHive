"""
Caso de uso: Obtener Usuario.

Obtiene un usuario por su ID o email.
"""

from typing import Optional

from ...domain.entities import User
from ...domain.repositories import UserRepositoryPort


class GetUserUseCase:
    """
    Caso de uso para obtener un usuario.
    """

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> Optional[User]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario

        Returns:
            El usuario si existe, None en caso contrario
        """
        return await self.user_repository.get_by_id(user_id)

    async def execute_by_id(self, user_id: str) -> Optional[User]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario

        Returns:
            El usuario si existe, None en caso contrario
        """
        return await self.user_repository.get_by_id(user_id)

    async def execute_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su correo electrónico.

        Args:
            email: Correo electrónico del usuario

        Returns:
            El usuario si existe, None en caso contrario
        """
        return await self.user_repository.get_by_email(email)

    async def execute_by_microsoft_id(self, microsoft_id: str) -> Optional[User]:
        """
        Obtiene un usuario por su ID de Microsoft.

        Args:
            microsoft_id: ID de Microsoft del usuario

        Returns:
            El usuario si existe, None en caso contrario
        """
        return await self.user_repository.get_by_microsoft_id(microsoft_id)
