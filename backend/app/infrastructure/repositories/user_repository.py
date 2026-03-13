"""
Repositorio de Usuarios para MongoDB.

Implementación del puerto UserRepositoryPort usando MongoDB.
"""

from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from ...domain.entities import User, RoleEnum
from ...domain.repositories import UserRepositoryPort


class UserRepository(UserRepositoryPort):
    """
    Implementación del repositorio de usuarios para MongoDB.
    """

    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.users

    def _to_entity(self, doc: dict) -> Optional[User]:
        """Convierte un documento MongoDB a entidad de dominio."""
        if not doc:
            return None

        return User(
            id=str(doc.get("_id", "")),
            name=doc.get("name", ""),
            email=doc.get("email", ""),
            microsoft_id=doc.get("microsoftId", ""),
            role=RoleEnum(doc.get("role", "student")),
            advisor_subjects=doc.get("advisorSubjects", []),
            created_at=doc.get("createdAt", datetime.now()),
            updated_at=doc.get("updatedAt", datetime.now()),
            password_hash=doc.get("password"),
        )

    def _to_document(self, user: User) -> dict:
        """Convierte una entidad de dominio a documento MongoDB."""
        doc = {
            "name": user.name,
            "email": user.email,
            "microsoftId": user.microsoft_id,
            "role": user.role.value,
            "advisorSubjects": user.advisor_subjects,
            "updatedAt": datetime.now(),
        }

        if user.password_hash:
            doc["password"] = user.password_hash

        if user.id:
            doc["_id"] = ObjectId(user.id)
        else:
            doc["createdAt"] = user.created_at

        return doc

    async def create(self, user: User) -> User:
        """Crea un nuevo usuario."""
        doc = self._to_document(user)
        doc["createdAt"] = datetime.now()

        result = await self.collection.insert_one(doc)
        user.id = str(result.inserted_id)
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(user_id)})
            return self._to_entity(doc)
        except Exception:
            return None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su correo electrónico."""
        doc = await self.collection.find_one({"email": email})
        return self._to_entity(doc)

    async def get_by_microsoft_id(self, microsoft_id: str) -> Optional[User]:
        """Obtiene un usuario por su ID de Microsoft."""
        doc = await self.collection.find_one({"microsoftId": microsoft_id})
        return self._to_entity(doc)

    async def update(self, user: User) -> User:
        """Actualiza un usuario existente."""
        doc = self._to_document(user)
        doc["updatedAt"] = datetime.now()

        await self.collection.replace_one({"_id": ObjectId(user.id)}, doc)
        return user

    async def delete(self, user_id: str) -> bool:
        """Elimina un usuario por su ID."""
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    async def list_all(self) -> List[User]:
        """Lista todos los usuarios."""
        cursor = self.collection.find()
        return [self._to_entity(doc) async for doc in cursor]

    async def list_by_role(self, role: RoleEnum) -> List[User]:
        """Lista usuarios por rol."""
        cursor = self.collection.find({"role": role.value})
        return [self._to_entity(doc) async for doc in cursor]

    async def list_advisors_by_subject(self, subject: str) -> List[User]:
        """Lista asesores que pueden enseñar una materia."""
        cursor = self.collection.find(
            {"role": RoleEnum.ADVISOR.value, "advisorSubjects": subject}
        )
        return [self._to_entity(doc) async for doc in cursor]
