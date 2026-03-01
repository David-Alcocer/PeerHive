from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from urllib.parse import quote
import os
import logging
import base64
import hashlib
import msal

# Configuration
class Settings(BaseSettings):
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://mongo:27017")
    DB_NAME: str = os.getenv("DB_NAME", "peerhive")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")

settings = Settings()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ── Cifrado de tokens ──────────────────────────────────────────────
# IMPORTANTE: La derivación de clave DEBE ser idéntica a la de app/config.py
# para que los tokens cifrados por el frontend-app puedan ser descifrados aquí.
_SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "dev-change-me")
_TOKEN_KEY_SOURCE = os.getenv("TOKEN_ENCRYPTION_KEY_RAW") or _SESSION_SECRET_KEY
_TOKEN_ENCRYPTION_KEY = base64.urlsafe_b64encode(
    hashlib.sha256(_TOKEN_KEY_SOURCE.encode()).digest()
)

# Instancia singleton de Fernet para evitar reconstruirla en cada llamada
from cryptography.fernet import Fernet as _Fernet
_fernet = _Fernet(_TOKEN_ENCRYPTION_KEY)


def _build_fernet() -> "_Fernet":
    """
    Retorna la instancia singleton de Fernet.

    Derivación de clave (debe coincidir con app/config.py):
      1. TOKEN_ENCRYPTION_KEY_RAW  (variable dedicada, recomendada en producción)
      2. SESSION_SECRET_KEY        (fallback, menos seguro — default "dev-change-me")
    """
    return _fernet


def _decrypt_token(encrypted_token: str) -> Optional[str]:
    """Descifra un token cifrado con Fernet. Retorna None si falla."""
    try:
        f = _build_fernet()
        return f.decrypt(encrypted_token.encode()).decode()
    except Exception as e:
        logger.warning(f"Error al descifrar token: {e}")
        return None


def _encrypt_token(token: str) -> str:
    """Cifra un token con Fernet."""
    f = _build_fernet()
    return f.encrypt(token.encode()).decode()


def _is_valid_jwt_format(token: str) -> bool:
    """
    Valida que el token tenga el formato básico de un JWT (3 partes separadas por '.').
    No verifica firma ni expiración — solo estructura mínima.
    """
    if not token or not isinstance(token, str):
        return False
    parts = token.split(".")
    if len(parts) != 3:
        logger.warning("Token rechazado: no tiene el formato JWT esperado (3 partes)")
        return False
    # Cada parte debe tener contenido
    if not all(parts):
        logger.warning("Token rechazado: alguna parte del JWT está vacía")
        return False
    return True


def get_access_token(request: Request) -> Optional[str]:
    """
    Extrae el token de acceso del header Authorization o de la sesión.

    Prioridad:
      1. Header 'Authorization: Bearer <token>' — validado como JWT básico.
      2. Sesión cifrada 'ms_graph_token' — descifrado con Fernet.
    """
    # Primero intentar obtener del header Authorization
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Extraer token después de "Bearer "
        if _is_valid_jwt_format(token):
            return token
        logger.warning("Token del header Authorization rechazado por formato inválido")

    # Fallback: verificar en la sesión
    encrypted_token = request.session.get("ms_graph_token")
    logger.info(f"Buscando token en sesión: {'encontrado' if encrypted_token else 'no encontrado'}")
    if encrypted_token:
        return _decrypt_token(encrypted_token)

    return None


def validate_token(token: str) -> bool:
    """
    Valida que el token no esté vacío y tenga un formato básico válido.
    
    Nota: Para validación completa de expiración, decodificar el JWT.
    """
    if not token or not isinstance(token, str):
        return False
    
    # Verificar longitud mínima (tokens de acceso típicos tienen al menos 20 caracteres)
    if len(token) < 20:
        logger.warning(f"Token demasiado corto: {len(token)} caracteres")
        return False
    
    # Los tokens JWT tienen 3 partes separadas por puntos
    # Esta es una validación básica, no exhaustiva
    return True

# Pydantic Models for Calendar API
class CalendarEventCreate(BaseModel):
    subject: str
    body: str
    start_datetime: str
    end_datetime: str
    location: Optional[str] = None
    attendees: Optional[List[Dict[str, str]]] = None
    is_online_meeting: bool = True
    online_meeting_provider: str = "teamsForBusiness"


class CalendarEventUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    start_datetime: Optional[str] = None
    end_datetime: Optional[str] = None
    location: Optional[str] = None
    attendees: Optional[List[Dict[str, str]]] = None
    is_online_meeting: Optional[bool] = None


class CalendarEventsRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None


# Pydantic Models for Teams API
class TeamsMeetingCreate(BaseModel):
    subject: str
    start_time: str
    end_time: str
    participants: Optional[List[Dict[str, str]]] = None

# App Initialization
app = FastAPI(title="PeerHive API", version="1.0.0")

# DBase Connection
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    print(f"Connected to MongoDB at {settings.MONGO_URL}")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    print("MongoDB connection closed")

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware for Microsoft Graph authentication
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="session",
    max_age=3600  # 1 hour
)

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to PeerHive API"}

@app.get("/health")
async def health():
    return {"status": "ok", "db": "connected" if app.mongodb else "disconnected"}


# Calendar API Routes
@app.get("/api/calendar/events")
async def get_calendar_events(
    request: Request,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Obtiene eventos del calendario de Outlook.
    
    Requiere que el usuario esté autenticado con Microsoft Graph.
    """
    # Obtener el token de acceso del header Authorization o sesión
    access_token = get_access_token(request)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado con Microsoft Graph. Por favor, inicia sesión primero."
        )
    
    try:
        from .services.calendar import get_calendar_events
        events = get_calendar_events(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )
        return {"events": events, "count": len(events)}
    except Exception as e:
        logger.error(f"Error fetching calendar events: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching calendar events: {str(e)}")


@app.post("/api/calendar/events")
async def create_calendar_event(request: Request, event: CalendarEventCreate):
    """
    Crea un nuevo evento de asesoría en el calendario de Outlook.
    
    Requiere que el usuario esté autenticado con Microsoft Graph.
    """
    # Obtener el token de acceso del header Authorization o sesión
    access_token = get_access_token(request)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado con Microsoft Graph. Por favor, inicia sesión primero."
        )
    
    try:
        from .services.calendar import create_calendar_event
        new_event = create_calendar_event(
            access_token=access_token,
            subject=event.subject,
            body=event.body,
            start_datetime=event.start_datetime,
            end_datetime=event.end_datetime,
            location=event.location,
            attendees=event.attendees,
            is_online_meeting=event.is_online_meeting,
            online_meeting_provider=event.online_meeting_provider
        )
        return {"event": new_event, "message": "Evento creado exitosamente"}
    except Exception as e:
        logger.error(f"Error creating calendar event: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating calendar event: {str(e)}")


@app.get("/api/calendar/events/{event_id}")
async def get_calendar_event(request: Request, event_id: str):
    """
    Obtiene un evento específico del calendario por su ID.
    """
    # Obtener el token de acceso del header Authorization o sesión
    access_token = get_access_token(request)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado con Microsoft Graph. Por favor, inicia sesión primero."
        )
    
    try:
        from .services.calendar import get_event_by_id
        event = get_event_by_id(access_token=access_token, event_id=event_id)
        return {"event": event}
    except Exception as e:
        logger.error(f"Error fetching calendar event: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching calendar event: {str(e)}")


@app.put("/api/calendar/events/{event_id}")
async def update_calendar_event(request: Request, event_id: str, event: CalendarEventUpdate):
    """
    Actualiza un evento existente en el calendario de Outlook.
    """
    # Obtener el token de acceso del header Authorization o sesión
    access_token = get_access_token(request)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado con Microsoft Graph. Por favor, inicia sesión primero."
        )
    
    try:
        from .services.calendar import update_calendar_event
        updated_event = update_calendar_event(
            access_token=access_token,
            event_id=event_id,
            subject=event.subject,
            body=event.body,
            start_datetime=event.start_datetime,
            end_datetime=event.end_datetime,
            location=event.location,
            attendees=event.attendees,
            is_online_meeting=event.is_online_meeting
        )
        return {"event": updated_event, "message": "Evento actualizado exitosamente"}
    except Exception as e:
        logger.error(f"Error updating calendar event: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating calendar event: {str(e)}")


@app.delete("/api/calendar/events/{event_id}")
async def delete_calendar_event(request: Request, event_id: str):
    """
    Elimina un evento del calendario de Outlook.
    """
    # Obtener el token de acceso del header Authorization o sesión
    access_token = get_access_token(request)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado con Microsoft Graph. Por favor, inicia sesión primero."
        )
    
    try:
        from .services.calendar import delete_calendar_event
        delete_calendar_event(access_token=access_token, event_id=event_id)
        return {"message": "Evento eliminado exitosamente"}
    except Exception as e:
        logger.error(f"Error deleting calendar event: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting calendar event: {str(e)}")


# Teams API Routes
@app.post("/api/teams/meetings")
async def create_teams_meeting(request: Request, meeting: TeamsMeetingCreate):
    """
    Crea una reunión de Microsoft Teams.
    
    Requiere que el usuario esté autenticado con Microsoft Graph.
    """
    # Obtener el token de acceso del header Authorization o sesión
    access_token = get_access_token(request)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado con Microsoft Graph. Por favor, inicia sesión primero."
        )
    
    try:
        from .services.teams import create_teams_meeting
        new_meeting = create_teams_meeting(
            access_token=access_token,
            subject=meeting.subject,
            start_time=meeting.start_time,
            end_time=meeting.end_time,
            participants=meeting.participants
        )
        return {"meeting": new_meeting, "message": "Reunión de Teams creada exitosamente"}
    except Exception as e:
        logger.error(f"Error creating Teams meeting: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating Teams meeting: {str(e)}")


@app.get("/api/teams/meetings/{meeting_id}")
async def get_teams_meeting(request: Request, meeting_id: str):
    """
    Obtiene los detalles de una reunión de Teams específica.
    """
    # Obtener el token de acceso del header Authorization o sesión
    access_token = get_access_token(request)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado con Microsoft Graph. Por favor, inicia sesión primero."
        )
    
    try:
        from .services.teams import get_meeting
        meeting = get_meeting(access_token=access_token, meeting_id=meeting_id)
        return {"meeting": meeting}
    except Exception as e:
        logger.error(f"Error fetching Teams meeting: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching Teams meeting: {str(e)}")


@app.get("/api/teams/meetings/{meeting_id}/attendance")
async def get_meeting_attendance(request: Request, meeting_id: str):
    """
    Obtiene los reportes de asistencia de una reunión de Teams.
    """
    # Obtener el token de acceso del header Authorization o sesión
    access_token = get_access_token(request)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado con Microsoft Graph. Por favor, inicia sesión primero."
        )
    
    try:
        from .services.teams import get_meeting_attendance_report
        reports = get_meeting_attendance_report(access_token=access_token, meeting_id=meeting_id)
        
        # Si hay reportes, obtener los detalles del primero
        if reports:
            first_report = reports[0]
            report_id = first_report.get("report_id")
            if report_id:
                from .services.teams import get_attendance_report_details
                details = get_attendance_report_details(
                    access_token=access_token, 
                    meeting_id=meeting_id, 
                    report_id=report_id
                )
                return {"attendance": details}
        
        return {"attendance": {"reports": reports, "message": "No hay reportes de asistencia disponibles"}}
    except Exception as e:
        logger.error(f"Error fetching attendance report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching attendance report: {str(e)}")


@app.get("/api/teams/meetings/{meeting_id}/attendance/{report_id}")
async def get_attendance_report(request: Request, meeting_id: str, report_id: str):
    """
    Obtiene los detalles de un reporte de asistencia específico.
    """
    # Obtener el token de acceso del header Authorization o sesión
    access_token = get_access_token(request)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado con Microsoft Graph. Por favor, inicia sesión primero."
        )
    
    try:
        from .services.teams import get_attendance_report_details
        report = get_attendance_report_details(
            access_token=access_token, 
            meeting_id=meeting_id, 
            report_id=report_id
        )
        return {"report": report}
    except Exception as e:
        logger.error(f"Error fetching attendance report details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching attendance report details: {str(e)}")


# Microsoft Graph Authentication Routes

# Azure Configuration
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
AUTHORITY = "https://login.microsoftonline.com/common"
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")
SCOPES = ["User.Read", "Calendars.ReadWrite", "OnlineMeetings.ReadWrite", "OnlineMeetingArtifact.Read.All"]


def build_msal_app():
    """Build MSAL application instance."""
    return msal.ConfidentialClientApplication(
        client_id=AZURE_CLIENT_ID,
        client_credential=AZURE_CLIENT_SECRET,
        authority=AUTHORITY,
    )


@app.get("/auth/login")
async def login(request: Request):
    """
    Inicia el flujo de autenticación con Microsoft Graph.
    """
    request.session.clear()
    
    msal_app = build_msal_app()
    flow = msal_app.initiate_auth_code_flow(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        prompt="login",
    )
    
    request.session["auth_flow"] = flow
    return {"auth_uri": flow["auth_uri"]}


@app.get("/auth/callback")
async def callback(request: Request):
    """
    Maneja el callback de Microsoft OAuth después de la autenticación.
    """
    flow = request.session.get("auth_flow")
    if not flow:
        raise HTTPException(status_code=400, detail="No auth flow. Ve a /auth/login otra vez.")
    
    msal_app = build_msal_app()
    try:
        result = msal_app.acquire_token_by_auth_code_flow(flow, dict(request.query_params))
    except ValueError:
        raise HTTPException(status_code=400, detail="State/CSRF validation failed.")
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error_description", result["error"]))
    
    claims = result.get("id_token_claims") or {}
    request.session["user"] = {
        "name": claims.get("name"),
        "email": claims.get("preferred_username") or claims.get("email"),
        "tid": claims.get("tid"),
        "oid": claims.get("oid"),
    }
    # Guardar el access_token de Microsoft Graph cifrado para uso en servicios
    access_token = result.get("access_token")
    if access_token:
        request.session["ms_graph_token"] = _encrypt_token(access_token)
        logger.info("Token de Microsoft Graph almacenado en sesión (cifrado)")
    
    return {"message": "Autenticación exitosa", "user": request.session["user"]}


@app.get("/auth/logout")
async def logout(request: Request):
    """
    Cierra la sesión del usuario.
    """
    request.session.clear()
    
    post_logout_redirect = "http://localhost:8000/"
    microsoft_logout = (
        "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={quote(post_logout_redirect)}"
    )
    
    return {"logout_uri": microsoft_logout}


@app.get("/auth/me")
async def get_current_user(request: Request):
    """
    Obtiene el usuario actual autenticado.
    """
    user = request.session.get("user")
    has_token = bool(request.session.get("ms_graph_token"))
    
    return {
        "user": user,
        "authenticated": bool(user),
        "has_graph_token": has_token
    }
