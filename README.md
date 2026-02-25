# PeerHive – Backend con Autenticación Microsoft
## Descripción General
En este proyecto se desarrolló un backend utilizando FastAPI que implementa autenticación con Microsoft Entra ID (OAuth 2.0 – Authorization Code Flow), manejo de sesiones seguras y documentación automática de la API mediante Swagger (OpenAPI 3.0).
El objetivo fue construir la base de una plataforma de asesorías académicas, donde únicamente usuarios autenticados puedan acceder a funcionalidades protegidas del sistema.

## Estructura del proyecto
```bash
PeerHive/
│
├── app/
│   ├── main.py        # Configuración principal de la aplicación
│   ├── auth.py        # Lógica de autenticación con Microsoft Entra
│   ├── asesorias.py   # Endpoints CRUD de asesorías
│   ├── config.py      # Variables de entorno y configuración
│   └── __init__.py
│
├── templates/
│   └── app.html       # Vista protegida para usuarios autenticados
│
├── .env               # Credenciales y configuración sensible
└── README.md
 ```
## Proceso
1. Redirigir al usuario a Microsoft para autenticación.
2. Recibir un código de autorización en el callback.
3. Intercambiar el código por un token usando la librería MSAL.
4. Extraer información del usuario.
5. Guardar los datos del usuario en sesión.
6. Proteger rutas verificando la existencia de sesión activa.
### Esto garantiza:
1. Validación segura mediante state (protección CSRF).
2. Manejo de sesión con cookies.
3. Protección de rutas privadas.

## Documentación de Endpoints (Swagger)
Se implementó documentación automática usando OpenAPI.
Disponible en:
```bash
/docs (Swagger UI interactivo
/redoc
/openapi.json
 ```
### Características implementadas:

1. Organización de endpoints por módulos usando APIRouter.
2. Modelos tipados con Pydantic.
3. Validación automática de datos.
4. Soporte para métodos HTTP: GET, POST y DELETE.
5. Esquemas JSON generados automáticamente.
6. Interfaz interactiva para probar endpoints desde el navegador.
## Endpoints Principales
### Autenticación
```bash
GET /auth/login

GET /auth/callback

GET /auth/logout

Gestión de Asesorías

GET /api/asesorias

POST /api/asesorias

DELETE /api/asesorias/{id}

Ruta Protegida
GET /app
 ```
 ** freddie Uitzil **

