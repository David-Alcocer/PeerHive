"""
Teams Service - Microsoft Graph API Integration
Gestión de reuniones de Teams y reportes de asistencia
"""

import requests
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

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


# Pydantic Models for Teams API
class AttendanceRecord(BaseModel):
    """Modelo para un registro de asistencia."""
    participant_id: str
    display_name: str
    email: str
    join_time: datetime
    leave_time: datetime
    attendance_time: Optional[datetime] = None
    role: str  # "attendee", "presenter", "organizer"


class TeamsMeetingCreate(BaseModel):
    """Modelo para crear una reunión de Teams."""
    subject: str
    start_time: str  # ISO 8601 format
    end_time: str    # ISO 8601 format
    participants: Optional[List[Dict[str, str]]] = None


def create_teams_meeting(
    access_token: str,
    subject: str,
    start_time: str,
    end_time: str,
    participants: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Crea una reunión de Microsoft Teams.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        subject: Título de la reunión
        start_time: Fecha/hora de inicio (formato ISO 8601: YYYY-MM-DDTHH:MM:SS)
        end_time: Fecha/hora de fin (formato ISO 8601: YYYY-MM-DDTHH:MM:SS)
        participants: Lista de participantes [{'email': 'email@example.com', 'role': 'attendee|presenter'}]
    
    Returns:
        Dict con los datos de la reunión creada (joinUrl, meetingId, audioConferencing info)
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/onlineMeetings"
    
    # Construir el cuerpo de la reunión
    meeting_data = {
        "subject": subject,
        "startDateTime": start_time,
        "endDateTime": end_time,
        "lobbyBypassSettings": {
            "scope": "organization",
            "isDialInBypassEnabled": True
        }
    }
    
    # Agregar participantes si se proporcionan
    if participants:
        attendee_list = []
        for participant in participants:
            attendee_list.append({
                "upn": participant["email"],
                "role": participant.get("role", "attendee")
            })
        meeting_data["attendees"] = {
            "attendees": attendee_list
        }
    
    logger.info(f"Creating Teams meeting: {subject}")
    
    try:
        response = requests.post(
            url,
            headers=get_headers(access_token),
            json=meeting_data,
            timeout=30
        )
        response.raise_for_status()
        
        meeting = response.json()
        logger.info(f"Teams meeting created successfully: {meeting.get('id')}")
        
        # Extraer información relevante
        return {
            "meeting_id": meeting.get("id"),
            "join_url": meeting.get("joinUrl"),
            "subject": meeting.get("subject"),
            "start_date_time": meeting.get("startDateTime"),
            "end_date_time": meeting.get("endDateTime"),
            "audio_conferencing": meeting.get("audioConferencing"),
            "video_teleconference_id": meeting.get("videoTeleconferenceId"),
            "chat_info": meeting.get("chatInfo"),
            "created_datetime": meeting.get("createdDateTime")
        }
        
    except requests.HTTPError as e:
        logger.error(f"Error creating Teams meeting: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating Teams meeting: {str(e)}")
        raise


def get_meeting(
    access_token: str,
    meeting_id: str
) -> Dict[str, Any]:
    """
    Obtiene los detalles de una reunión de Teams específica.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        meeting_id: ID de la reunión de Teams
    
    Returns:
        Dict con los datos de la reunión
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/onlineMeetings/{meeting_id}"
    
    logger.info(f"Fetching Teams meeting: {meeting_id}")
    
    try:
        response = requests.get(
            url,
            headers=get_headers(access_token),
            timeout=30
        )
        response.raise_for_status()
        
        meeting = response.json()
        logger.info(f"Retrieved Teams meeting: {meeting_id}")
        
        return {
            "meeting_id": meeting.get("id"),
            "join_url": meeting.get("joinUrl"),
            "subject": meeting.get("subject"),
            "start_date_time": meeting.get("startDateTime"),
            "end_date_time": meeting.get("endDateTime"),
            "audio_conferencing": meeting.get("audioConferencing"),
            "video_teleconference_id": meeting.get("videoTeleconferenceId"),
            "chat_info": meeting.get("chatInfo"),
            "created_datetime": meeting.get("createdDateTime")
        }
        
    except requests.HTTPError as e:
        logger.error(f"Error fetching Teams meeting: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching Teams meeting: {str(e)}")
        raise


def get_meeting_attendance_report(
    access_token: str,
    meeting_id: str
) -> List[Dict[str, Any]]:
    """
    Obtiene los reportes de asistencia de una reunión de Teams.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        meeting_id: ID de la reunión de Teams
    
    Returns:
        Lista de reportes de asistencia
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/onlineMeetings/{meeting_id}/attendanceReports"
    
    logger.info(f"Fetching attendance reports for meeting: {meeting_id}")
    
    try:
        response = requests.get(
            url,
            headers=get_headers(access_token),
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        reports = data.get("value", [])
        
        logger.info(f"Retrieved {len(reports)} attendance reports")
        
        # Extraer información relevante de cada reporte
        return [
            {
                "report_id": report.get("id"),
                "meeting_id": report.get("meetingId"),
                "total_participant_count": report.get("totalParticipantCount"),
                "attendance_records": report.get("attendanceRecords", [])
            }
            for report in reports
        ]
        
    except requests.HTTPError as e:
        logger.error(f"Error fetching attendance reports: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching attendance reports: {str(e)}")
        raise


def get_attendance_report_details(
    access_token: str,
    meeting_id: str,
    report_id: str
) -> Dict[str, Any]:
    """
    Obtiene los detalles del reporte de asistencia de una reunión de Teams.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        meeting_id: ID de la reunión de Teams
        report_id: ID del reporte de asistencia
    
    Returns:
        Dict con los detalles del reporte de asistencia
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/onlineMeetings/{meeting_id}/attendanceReports/{report_id}"
    
    logger.info(f"Fetching attendance report details: {report_id} for meeting: {meeting_id}")
    
    try:
        response = requests.get(
            url,
            headers=get_headers(access_token),
            timeout=30
        )
        response.raise_for_status()
        
        report = response.json()
        logger.info(f"Retrieved attendance report details: {report_id}")
        
        # Procesar los registros de asistencia
        attendance_records = []
        for record in report.get("attendanceRecords", []):
            # Extraer información del participante
            identity = record.get("identity", {})
            email = ""
            display_name = ""
            
            if identity.get("user"):
                email = (identity.get("user", {}).get("mail") or
                         identity.get("user", {}).get("userPrincipalName") or
                         identity.get("user", {}).get("id", ""))
                display_name = identity.get("user", {}).get("displayName", "")
            
            # Obtener tiempos de entrada y salida
            attendance_intervals = record.get("attendanceIntervalRecords", [])
            join_time = None
            leave_time = None
            
            if attendance_intervals:
                first_interval = attendance_intervals[0]
                join_time = first_interval.get("joinDateTime")
                leave_time = attendance_intervals[-1].get("leaveDateTime") if len(attendance_intervals) > 1 else first_interval.get("leaveDateTime")
            
            attendance_records.append({
                "participant_id": record.get("id", ""),
                "display_name": display_name,
                "email": email,
                "join_time": join_time,
                "leave_time": leave_time,
                "attendance_time": join_time,  # Primer tiempo de entrada
                "role": record.get("role", "attendee")
            })
        
        return {
            "report_id": report.get("id"),
            "meeting_id": report.get("meetingId"),
            "total_participant_count": report.get("totalParticipantCount"),
            "attendance_records": attendance_records
        }
        
    except requests.HTTPError as e:
        logger.error(f"Error fetching attendance report details: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching attendance report details: {str(e)}")
        raise


def list_teams_meetings(
    access_token: str,
    filter_query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Lista las reuniones de Teams del usuario.
    
    Args:
        access_token: Token de acceso de Microsoft Graph
        filter_query: Query filter adicional (opcional)
    
    Returns:
        Lista de reuniones de Teams
    
    Raises:
        requests.HTTPError: Si la API retorna un error
    """
    url = f"{GRAPH_API_BASE_URL}/me/onlineMeetings"
    
    params = {
        "$select": "id,subject,startDateTime,endDateTime,joinUrl,createdDateTime"
    }
    
    if filter_query:
        params["$filter"] = filter_query
    
    logger.info("Fetching Teams meetings")
    
    try:
        response = requests.get(
            url,
            headers=get_headers(access_token),
            params=params,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        meetings = data.get("value", [])
        
        logger.info(f"Retrieved {len(meetings)} Teams meetings")
        return meetings
        
    except requests.HTTPError as e:
        logger.error(f"Error fetching Teams meetings: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching Teams meetings: {str(e)}")
        raise
