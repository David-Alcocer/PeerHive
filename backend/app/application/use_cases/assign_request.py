"""
Caso de uso: Asignar Solicitud.

Asigna una solicitud de asesoría a un asesor.
"""

from ...domain.entities import Request
from ...domain.repositories import RequestRepositoryPort


class AssignRequestUseCase:
    """
    Caso de uso para asignar una solicitud a un asesor.
    """

    def __init__(self, request_repository: RequestRepositoryPort):
        self.request_repository = request_repository

    async def execute(self, request_id: str, advisor_id: str) -> Request:
        """
        Ejecuta el caso de uso para asignar una solicitud.

        Args:
            request_id: ID de la solicitud a asignar
            advisor_id: ID del asesor al que se asigna

        Returns:
            La solicitud actualizada

        Raises:
            ValueError: Si la solicitud no existe o ya está asignada
        """
        # Verificar que la solicitud existe
        request = await self.request_repository.get_by_id(request_id)
        if not request:
            raise ValueError("La solicitud no existe")

        # Verificar que la solicitud está pendiente
        # Soporta tanto entidades Request (con .is_pending()) como dicts
        if isinstance(request, dict):
            if request.get("status") != "pending":
                raise ValueError("Request already assigned")
        else:
            if not request.is_pending():
                raise ValueError("Request already assigned")

        # Asignar la solicitud al asesor
        updated_request = await self.request_repository.update(
            request_id, {"status": "assigned", "advisor_id": advisor_id}
        )

        return updated_request
