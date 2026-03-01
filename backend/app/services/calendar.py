"""
Calendar Service - Microsoft Graph API Integration
Sincronización de eventos del calendario con Outlook Calendar
"""

import requests
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Microsoft Graph API Base URL
GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0"

# Headers for Graph API requests
def get_headers(access_token: str, timezone: str = "UTC") -> Dict[str, str]:
    """Get headers for Microsoft Graph API requests."""
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": f'outlook.timezone="{timezone}"'
    }


def get_calendar_events(
    access_token: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    filter_query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Obtiene eventos del calendario de Outlook.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        start_date: Fecha de inicio (formato ISO 8601: YYYY-MM-DD)
        end_date: Fecha de fin (formato ISO 8601: YYYY-MM-DD)
        filter_query: Query filter adicional (ej: "subject eq 'Asesoría'")
    
    Returns:
        Lista de eventos del calendario
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/calendar/events"
    
    # Construir parámetros de query
    params = {
        "$select": "id,subject,body,start,end,location,organizer,attendees,isOnlineMeeting,onlineMeeting",
        "$orderby": "start/dateTime"
    }
    
    # Agregar filtro de fechas si se proporciona
    if start_date and end_date:
        # Filtrar eventos en un rango de fechas
        params["$filter"] = f"start/dateTime ge '{start_date}T00:00:00' and end/dateTime le '{end_date}T23:59:59'"
    elif filter_query:
        params["$filter"] = filter_query
    
    logger.info(f"Fetching calendar events from {start_date} to {end_date}")
    
    try:
        response = requests.get(
            url,
            headers=get_headers(access_token),
            params=params,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        events = data.get("value", [])
        
        logger.info(f"Retrieved {len(events)} calendar events")
        return events
        
    except requests.HTTPError as e:
        logger.error(f"Error fetching calendar events: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching calendar events: {str(e)}")
        raise


def create_calendar_event(
    access_token: str,
    subject: str,
    body: str,
    start_datetime: str,
    end_datetime: str,
    location: Optional[str] = None,
    attendees: Optional[List[Dict[str, str]]] = None,
    is_online_meeting: bool = True,
    online_meeting_provider: str = "teamsForBusiness"
) -> Dict[str, Any]:
    """
    Crea un evento de asesoría en el calendario de Outlook.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        subject: Título del evento
        body: Descripción del evento
        start_datetime: Fecha/hora de inicio (formato ISO 8601: YYYY-MM-DDTHH:MM:SS)
        end_datetime: Fecha/hora de fin (formato ISO 8601: YYYY-MM-DDTHH:MM:SS)
        location: Ubicación física (opcional)
        attendees: Lista de asistentes [{'email': 'email@example.com', 'type': 'required|optional'}]
        is_online_meeting: Si es reunión online (Teams)
        online_meeting_provider: Proveedor de reunión online (teamsForBusiness, skypeForBusiness)
    
    Returns:
        Dict con los datos del evento creado
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/calendar/events"
    
    # Construir el cuerpo del evento
    event_data = {
        "subject": subject,
        "body": {
            "contentType": "HTML",
            "content": body
        },
        "start": {
            "dateTime": start_datetime,
            "timeZone": "America/Mexico_City"
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": "America/Mexico_City"
        },
        "isOnlineMeeting": is_online_meeting,
        "onlineMeetingProvider": online_meeting_provider if is_online_meeting else None
    }
    
    # Agregar ubicación si se proporciona
    if location:
        event_data["location"] = {
            "displayName": location
        }
    
    # Agregar asistentes si se proporcionan
    if attendees:
        event_data["attendees"] = [
            {
                "emailAddress": {"address": attendee["email"]},
                "type": attendee.get("type", "required")
            }
            for attendee in attendees
        ]
    
    logger.info(f"Creating calendar event: {subject}")
    
    try:
        response = requests.post(
            url,
            headers=get_headers(access_token),
            json=event_data,
            timeout=30
        )
        response.raise_for_status()
        
        event = response.json()
        logger.info(f"Event created successfully: {event.get('id')}")
        return event
        
    except requests.HTTPError as e:
        logger.error(f"Error creating calendar event: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating calendar event: {str(e)}")
        raise


def update_calendar_event(
    access_token: str,
    event_id: str,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    start_datetime: Optional[str] = None,
    end_datetime: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[List[Dict[str, str]]] = None,
    is_online_meeting: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Actualiza un evento existente en el calendario de Outlook.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        event_id: ID del evento a actualizar
        subject: Nuevo título del evento (opcional)
        body: Nueva descripción del evento (opcional)
        start_datetime: Nueva fecha/hora de inicio (opcional)
        end_datetime: Nueva fecha/hora de fin (opcional)
        location: Nueva ubicación (opcional)
        attendees: Nuevos asistentes (opcional)
        is_online_meeting: Si es reunión online (opcional)
    
    Returns:
        Dict con los datos del evento actualizado
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/calendar/events/{event_id}"
    
    # Construir el cuerpo de actualización dinámicamente
    update_data = {}
    
    if subject is not None:
        update_data["subject"] = subject
    
    if body is not None:
        update_data["body"] = {
            "contentType": "HTML",
            "content": body
        }
    
    if start_datetime is not None:
        update_data["start"] = {
            "dateTime": start_datetime,
            "timeZone": "America/Mexico_City"
        }
    
    if end_datetime is not None:
        update_data["end"] = {
            "dateTime": end_datetime,
            "timeZone": "America/Mexico_City"
        }
    
    if location is not None:
        update_data["location"] = {
            "displayName": location
        }
    
    if attendees is not None:
        update_data["attendees"] = [
            {
                "emailAddress": {"address": attendee["email"]},
                "type": attendee.get("type", "required")
            }
            for attendee in attendees
        ]
    
    if is_online_meeting is not None:
        update_data["isOnlineMeeting"] = is_online_meeting
    
    logger.info(f"Updating calendar event: {event_id}")
    
    try:
        response = requests.patch(
            url,
            headers=get_headers(access_token),
            json=update_data,
            timeout=30
        )
        response.raise_for_status()
        
        event = response.json()
        logger.info(f"Event updated successfully: {event_id}")
        return event
        
    except requests.HTTPError as e:
        logger.error(f"Error updating calendar event: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating calendar event: {str(e)}")
        raise


def delete_calendar_event(
    access_token: str,
    event_id: str
) -> bool:
    """
    Elimina un evento del calendario de Outlook.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        event_id: ID del evento a eliminar
    
    Returns:
        True si la eliminación fue exitosa
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/calendar/events/{event_id}"
    
    logger.info(f"Deleting calendar event: {event_id}")
    
    try:
        response = requests.delete(
            url,
            headers=get_headers(access_token),
            timeout=30
        )
        response.raise_for_status()
        
        logger.info(f"Event deleted successfully: {event_id}")
        return True
        
    except requests.HTTPError as e:
        logger.error(f"Error deleting calendar event: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting calendar event: {str(e)}")
        raise


def get_event_by_id(
    access_token: str,
    event_id: str
) -> Dict[str, Any]:
    """
    Obtiene un evento específico del calendario por su ID.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        event_id: ID del evento a obtener
    
    Returns:
        Dict con los datos del evento
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/calendar/events/{event_id}"
    
    logger.info(f"Fetching calendar event: {event_id}")
    
    try:
        response = requests.get(
            url,
            headers=get_headers(access_token),
            timeout=30
        )
        response.raise_for_status()
        
        event = response.json()
        logger.info(f"Retrieved event: {event_id}")
        return event
        
    except requests.HTTPError as e:
        logger.error(f"Error fetching calendar event: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching calendar event: {str(e)}")
        raise
