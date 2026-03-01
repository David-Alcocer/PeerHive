# Documentación Técnica: Integración Microsoft Graph API

Este documento detalla la arquitectura, los cambios realizados, el estado actual y las limitaciones de la integración de Microsoft Graph API (Teams y Outlook Calendar) en PeerHive, implementada el 2026-02-28.

---

## 🏗 Arquitectura de la Integración

La integración se diseñó para conectar el sistema de asesorías local de PeerHive con el ecosistema de productividad de Microsoft 365, automatizando la creación de reuniones y eventos en el calendario.

### Flujo de Datos Principal
1. **Autenticación (OAuth 2.0 Auth Code Flow):** 
   - El usuario inicia sesión a través de `/auth/login` (redirigido a Microsoft).
   - El callback guarda la información del usuario en la sesión (`app/auth.py`).
   - Se obtiene un `access_token` de Microsoft Graph, el cual es **cifrado con Fernet** antes de almacenarse en la sesión local.

2. **Verificación de Estado:**
   - El frontend consume el endpoint `/auth/me` para determinar si el usuario tiene un token de Graph válido.
   - Si es así, las funciones de creación de sesiones activan la integración.

3. **Ejecución de Operaciones Múltiples:**
   - Al asignar una asesoría (`src/ui/requests.js` -> `assignRequestToAdvisor`), se ejecutan llamadas asíncronas no bloqueantes a:
     - `POST /api/teams/meetings` para generar el enlace de Teams.
     - `POST /api/calendar/events` para reservar el espacio en Outlook.

4. **Visualización:**
   - El calendario (`src/ui/calendar.js`) combina y renderiza en verde las sesiones locales y en azul los eventos obtenidos directamente desde Outlook vía `GET /api/calendar/events`.

---

## 📝 Resumen de Cambios y Adiciones

### Módulos y Paquetes Nuevos
- Se instalaron dependencias críticas: `msal` (Autenticación Microsoft), `cryptography` (Cifrado Fernet), `starlette` (Manejo robusto de sesiones) y `itsdangerous` (Firma de sesiones).
- Se crearon servicios modulares en el backend:
  - `backend/app/services/calendar.py`: Lógica pura de interacción con Outlook.
  - `backend/app/services/teams.py`: Lógica de creación de reuniones y reportes de Teams.

### Cambios Clave en Backend
- Implementación de Middleware de Sesiones (`SessionMiddleware`) en la API (`backend/app/main.py`).
- Implementación de funciones de descifrado simétrico para extraer el token de manera segura en cada request.
- Creación de 8 endpoints nuevos dedicados a la interacción proxy con Graph API.

### Cambios Clave en Frontend
- Configuración de URLs dinámicas (`config.js`).
- Extensión de `RequestService` (`src/services/request.service.js`) para manejar las nuevas llamadas a la API de backend.
- Modificación del flujo de la UI de *Solicitudes* para manejar la asignación multicanal sin bloquear el hilo principal ante fallos de red hacia Microsoft.

---

## ⚠️ Limitaciones y Advertencias (Estado Actual)

1. **Credenciales en Desarrollo:**
   - El archivo `.env` actualmente posee valores *dummy* (falsos) como `AZURE_CLIENT_ID=test-client-id`.
   - **Efecto:** El flujo de autenticación real y la creación de eventos en Microsoft fallarán o serán simulados hasta que se configuren credenciales válidas de un Tenant de Azure real.

2. **Doble Instancia de Autenticación:**
   - El endpoint `/auth/me` existe tanto en la aplicación principal (`app/main.py`) como en la API (`backend/app/main.py`).
   - **Advertencia:** Esto puede causar conflictos de enrutamiento o CORS si se fusionan las aplicaciones o si no se tiene claro a qué puerto se hacen las llamadas desde el cliente.

3. **Cookies de Sesión Inconsistentes:**
   - La aplicación frontend setea la cookie como `peerhive_session`.
   - La API del backend espera y maneja la cookie como `session`.
   - **Efecto:** El token de Graph obtenido en la interfaz de login podría no estar disponible para el backend si las sesiones no comparten el mismo nombre y dominio de cookie.

4. **Duplicación de Lógica Criptográfica:**
   - Las funciones de cifrado y descifrado de Fernet están escritas de forma independiente en `app/config.py` y `backend/app/main.py`.
   - **Advertencia:** Si cambia la salt o el método de derivación en un archivo y no en el otro, los tokens se corromperán y todas las llamadas a Graph fallarán silenciosamente con errores 401.

5. **Base de Datos Limpia en Docker:**
   - Al ejecutar localmente o vía Compose, la base de datos de MongoDB inicia vacía. Se debe crear un script de `seed` si se requiere ambiente de pruebas inmediato con data existente.

---

## 🛠 Cosas por Mejorar (Próximos Pasos)

1. **Refactorización de Autenticación y Cifrado (Prioridad Alta):**
   - Extraer la lógica de autenticación JWT/Fernet a un paquete compartido (ej. `shared/security.py`) que sea importado tanto por `app/` como por `backend/app/` para respetar el principio DRY.
   
2. **Unificar Nomenclatura de Sesiones:**
   - Configurar `SessionMiddleware` en ambos lados para usar explícitamente el mismo nombre de cookie (`peerhive_session`).
   
3. **Limpieza de Código:**
   - Remover la constante `GRAPH_API_URL` de `src/api/config.js` si todas las peticiones continuarán pasando a través del backend como proxy proxy (práctica recomendada).
   - Eliminar, documentar o exponer la función huérfana `list_teams_meetings()` dentro de `backend/app/services/teams.py`.

4. **Validación Exhaustiva de Fallos:**
   - Asegurar que si la creación del evento de Outlook falla, al menos el de Teams se complete y persista la configuración local para permitir trabajo degradado sin afectar la experiencia del usuario. Manejar *Retries* asíncronos para Graph API.
