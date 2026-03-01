# Changelog - Integración Microsoft Graph API

## Resumen General

Este changelog documenta todos los cambios implementados para integrar Microsoft Graph API (Outlook Calendar y Microsoft Teams) en PeerHive.

**Fecha de implementación:** 2026-02-28  
**Rama:** `dev_axel`  
**Total de cambios:** +875 líneas, -36 líneas

---

## Archivos Modificados (10)

### 1. `app/auth.py` (+18 líneas)
**Propósito:** Autenticación con Microsoft Entra ID

**Cambios:**
- ✅ Importación de módulo `logging`
- ✅ Importación de función `encrypt_token` desde `config.py`
- ✅ Agregado `logger` para registro de errores
- ✅ **NUEVO:** Cifrado del `access_token` de Microsoft Graph antes de guardarlo en sesión
- ✅ Manejo de errores en el cifrado de tokens

```python
# Nuevo código agregado
access_token = result.get("access_token")
if access_token:
    try:
        request.session["ms_graph_token"] = encrypt_token(access_token)
    except Exception as e:
        logger.error(f"Error cifrando access_token de Graph: {e}")
```

---

### 2. `app/config.py` (+40 líneas)
**Propósito:** Configuración centralizada y cifrado de tokens

**Cambios:**
- ✅ Importaciones: `logging`, `base64`, `hashlib`, `cryptography.fernet`
- ✅ **NUEVO:** Derivación de clave de cifrado (SHA256 + base64 URL-safe)
- ✅ **NUEVO:** Instancia singleton de Fernet para cifrado
- ✅ **NUEVO:** scopes de Graph expandidos:
  - `User.Read`
  - `Calendars.ReadWrite`
  - `OnlineMeetings.ReadWrite`
  - `OnlineMeetingArtifact.Read.All`
- ✅ **NUEVO:** Función `encrypt_token(token: str) -> str`
- ✅ **NUEVO:** Función `decrypt_token(encrypted_token: str) -> str`

```python
# Clave de cifrado para tokens
_token_key_source = os.getenv("TOKEN_ENCRYPTION_KEY_RAW") or SESSION_SECRET_KEY
TOKEN_ENCRYPTION_KEY = base64.urlsafe_b64encode(
    hashlib.sha256(_token_key_source.encode()).digest()
)
_fernet = Fernet(TOKEN_ENCRYPTION_KEY)
```

---

### 3. `app/main.py` (+18 líneas) [NUEVO ENDPOINT]
**Propósito:** Punto de entrada de la aplicación

**Cambios:**
- ✅ **NUEVO ENDPOINT:** `/auth/me` - Consulta estado de autenticación Graph

```python
@app.get("/auth/me")
async def get_current_user(request: Request):
    user = request.session.get("user")
    has_token = bool(request.session.get("ms_graph_token"))
    return {
        "user": user,
        "authenticated": bool(user),
        "has_graph_token": has_token
    }
```

---

### 4. `backend/app/main.py` (+530 líneas)
**Propósito:** API REST del backend con integración Graph

**Cambios mayores:**
- ✅ Importaciones de Microsoft Graph: `msal`, `requests`, `logging`, `base64`, `hashlib`
- ✅ **NUEVO:** Middleware de sesiones (Starlette)
- ✅ **NUEVO:** Modelo Pydantic `CalendarEventCreate`
- ✅ **NUEVO:** Modelo Pydantic `TeamsMeetingCreate`
- ✅ **NUEVO:** Funciones de cifrado/descifrado de tokens
- ✅ **NUEVO:** Función `_is_valid_jwt_format()` para validación de tokens
- ✅ **NUEVO:** Función `get_access_token()` - Extrae token del header o sesión

**NUEVOS ENDPOINTS:**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/calendar/events` | Obtiene eventos de Outlook |
| POST | `/api/calendar/events` | Crea evento en Outlook |
| GET | `/api/calendar/events/{event_id}` | Obtiene evento específico |
| PUT | `/api/calendar/events/{event_id}` | Actualiza evento |
| DELETE | `/api/calendar/events/{event_id}` | Elimina evento |
| POST | `/api/teams/meetings` | Crea reunión de Teams |
| GET | `/api/teams/meetings/{meeting_id}` | Obtiene detalles de reunión |
| GET | `/api/teams/meetings/{meeting_id}/attendance` | Obtiene reporte de asistencia |
| GET | `/auth/login` | Inicia flujo OAuth |
| GET | `/auth/callback` | Maneja callback OAuth |
| GET | `/auth/logout` | Cierra sesión |
| GET | `/auth/me` | Obtiene usuario actual y estado Graph |

---

### 5. `backend/requirements.txt` (+5 líneas)
**Propósito:** Dependencias de Python

**Nuevas dependencias:**
- `requests>=2.31.0`
- `msal>=1.28.0`
- `python-dotenv>=1.0.0`
- `starlette>=0.35.0`
- `cryptography>=42.0.0`

---

### 6. `src/api/config.js` (+2 líneas)
**Propósito:** Configuración de URLs del API

**Nuevas constantes:**
```javascript
export const API_BASE_URL = 'http://localhost:8000/api';
export const GRAPH_API_URL = 'https://graph.microsoft.com/v1.0';
```

---

### 7. `src/services/auth.service.js` (+24 líneas)
**Propósito:** Servicio de autenticación del frontend

**Nuevas funciones:**
- ✅ Importación de `API_URL`
- ✅ Función `checkGraphAuthStatus()` - Verifica si el usuario tiene sesión Graph activa

```javascript
export async function checkGraphAuthStatus() {
    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            method: 'GET',
            credentials: 'include'
        });
        if (!response.ok) return false;
        const data = await response.json();
        return data.has_graph_token === true;
    } catch (error) {
        console.warn('Error verificando estado de autenticación Graph:', error.message);
        return false;
    }
}
```

---

### 8. `src/services/request.service.js` (+105 líneas)
**Propósito:** Servicio de solicitudes y gestión de calendar/teams

**Nuevos métodos:**
- ✅ `getCalendarEvents(startDate, endDate)` - Obtiene eventos de Outlook
- ✅ `createCalendarEvent(eventData)` - Crea evento en Outlook
- ✅ `createTeamsMeeting(subject, startTime, endTime)` - Crea reunión de Teams
- ✅ `getMeetingAttendance(meetingId)` - Obtiene asistencia de reunión

---

### 9. `src/ui/calendar.js` (+103 líneas, -38 líneas)
**Propósito:** Interfaz de calendario

**Cambios:**
- ✅ Importaciones de `RequestService` y `API_BASE_URL`
- ✅ **NUEVO:** Función `loadGraphCalendarEvents()` - Carga eventos de Outlook
- ✅ **NUEVO:** Función `renderSessionList()` - Renderiza lista de sesiones
- ✅ Renderizado de eventos de Outlook con color azul (#2196F3)
- ✅ Renderizado de sesiones locales con color verde (#4CAF50)

---

### 10. `src/ui/requests.js` (+66 líneas)
**Propósito:** Interfaz de solicitudes

**Cambios en `assignRequestToAdvisor()`:**
- ✅ Obtención de datos de la solicitud
- ✅ Creación automática de reunión de Teams (no bloqueante)
- ✅ Creación automática de evento en calendario (no bloqueante)
- ✅ Actualización de sesión con link de Teams dinámico
- ✅ Mensajes de toast diferenciados según éxito/parcial/fallo

---

## Archivos Nuevos (3)

### 1. `backend/app/services/__init__.py` (1 línea)
```python
# Services package
```

### 2. `backend/app/services/calendar.py` (355 líneas)
**Funciones exportadas:**
- `get_calendar_events()` - Obtiene eventos del calendario
- `create_calendar_event()` - Crea nuevo evento
- `get_event_by_id()` - Obtiene evento por ID
- `update_calendar_event()` - Actualiza evento
- `delete_calendar_event()` - Elimina evento

### 3. `backend/app/services/teams.py` (368 líneas)
**Funciones exportadas:**
- `create_teams_meeting()` - Crea reunión de Teams
- `get_meeting()` - Obtiene detalles de reunión
- `get_meeting_attendance_report()` - Obtiene reporte de asistencia
- `get_attendance_report_details()` - Obtiene detalles de asistencia

---

## Cambios en Seguridad

### ✅ Implementado
1. **Cifrado de tokens:** Tokens de Microsoft Graph almacenados cifrados con Fernet
2. **Validación de JWT:** Validación de formato JWT antes de usar tokens
3. **CORS restrictivo:** Origen limitado a `localhost:3000` y `127.0.0.1:3000`
4. **Logging de errores:** Registro de errores de cifrado y autenticación
5. **Manejo de errores:** Operaciones secundarias (Teams/Calendar) no bloquean el flujo principal

### ⚠️ Notas de Seguridad
1. **Clave de cifrado:** En desarrollo usa `SESSION_SECRET_KEY` como fallback. En producción configurar `TOKEN_ENCRYPTION_KEY_RAW`
2. **Secret Key:** El backend usa `SECRET_KEY` separada de `SESSION_SECRET_KEY`

---

## Flujo de Datos

```
Usuario inicia sesión
       ↓
Microsoft OAuth (app/auth.py)
       ↓
Token cifrado con Fernet → Sesión
       ↓
Frontend consulta /auth/me
       ↓
Si has_graph_token=true:
  - Crear reunión Teams → /api/teams/meetings
  - Crear evento Calendar → /api/calendar/events
  - Sincronizar calendario → /api/calendar/events
```

---

## Endpoints de API

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/auth/login` | Redirige a Microsoft |
| GET | `/auth/callback` | Procesa OAuth |
| GET | `/auth/logout` | Cierra sesión |
| GET | `/auth/me` | Estado de auth (NUEVO) |

### Calendario (Graph API)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/calendar/events` | Lista eventos |
| POST | `/api/calendar/events` | Crea evento |
| GET | `/api/calendar/events/{id}` | Obtiene evento |
| PUT | `/api/calendar/events/{id}` | Actualiza evento |
| DELETE | `/api/calendar/events/{id}` | Elimina evento |

### Teams (Graph API)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/teams/meetings` | Crea reunión |
| GET | `/api/teams/meetings/{id}` | Obtiene reunión |
| GET | `/api/teams/meetings/{id}/attendance` | Reporte asistencia |

---

## Dependencias Externas

| Paquete | Versión | Uso |
|---------|---------|-----|
| `msal` | >=1.28.0 | Autenticación Microsoft |
| `requests` | >=2.31.0 | HTTP client para Graph API |
| `cryptography` | >=42.0.0 | Cifrado Fernet |
| `starlette` | >=0.35.0 | Middleware de sesiones |
| `python-dotenv` | >=1.0.0 | Variables de entorno |

---

## Variables de Entorno Requeridas

### Para `app/` (Autenticación)
```bash
AZURE_TENANT_ID=          # Tenant de Azure AD
AZURE_CLIENT_ID=          # Client ID de la app registrada
AZURE_CLIENT_SECRET=      # Secret de la app registrada
REDIRECT_URI=             # URL de callback
SESSION_SECRET_KEY=       # Clave para sesiones
TOKEN_ENCRYPTION_KEY_RAW= # Clave para cifrado (producción)
```

### Para `backend/app/` (API)
```bash
MONGO_URL=                # URL de MongoDB
DB_NAME=                  # Nombre de la base de datos
SECRET_KEY=               # Clave para sesiones del backend
AZURE_CLIENT_ID=          # Client ID
AZURE_CLIENT_SECRET=      # Secret
SESSION_SECRET_KEY=       # Debe coincidir con app/
TOKEN_ENCRYPTION_KEY_RAW= # Debe coincidir con app/
```

---

## Notas de Implementación

1. **Consistencia de cifrado:** La derivación de clave usa el mismo algoritmo en `app/config.py` y `backend/app/main.py` para permitir descifrado cruzado.

2. **Fallbacks seguros:** Si `TOKEN_ENCRYPTION_KEY_RAW` no está configurado, usa `SESSION_SECRET_KEY` (menos seguro, solo para desarrollo).

3. **Operaciones no bloqueantes:** La creación de reuniones Teams y eventos Calendar en el frontend no bloquea la asignación de asesores.

4. **Dos aplicaciones:** El proyecto tiene dos apps FastAPI (`app/` y `backend/app/`) que comparten lógica de autenticación pero sirven propósitos diferentes.
