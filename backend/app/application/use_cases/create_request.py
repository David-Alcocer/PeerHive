"""
Caso de uso: Crear Solicitud.

Crea una nueva solicitud de asesoría.
"""
from datetime import datetime

from ...domain.entities import Request, RequestStatusEnum
from ...domain.repositories import RequestRepositoryPort


class CreateRequestUseCase:
    """
    Caso de uso para crear una nueva solicitud de asesoría.
    """
    
    def __init__(self, request_repository: RequestRepositoryPort):
        self.request_repository = request_repository
    
    async def execute(
        self,
        student_id: str,
        subject: str,
        topic: str,
        description: str = None
    ) -> Request:
        """
        Ejecuta el caso de uso para crear una solicitud.
        
        Args:
            student_id: ID del estudiante que hace la solicitud
            subject: Materia de la asesoría
            topic: Tema específico
            description: Descripción adicional
            
        Returns:
            La solicitud creada
        """
        # Crear la entidad de dominio
        request = Request(
            student_id=student_id,
            subject=subject,
            topic=topic,
            description=description,
            status=RequestStatusEnum.PENDING,
            created_at=datetime.now()
        )
        
        # Persistir la solicitud
        created_request = await self.request_repository.create(request)
        
        return created_request
