# PeerHive – Plataforma de Asesorías Académicas

## Descripción General

PeerHive es una plataforma de asesorías académicas peer-to-peer que conecta estudiantes con asesores para mejorar el aprendizaje. El sistema cuenta con un backend FastAPI con MongoDB y un frontend Vanilla JavaScript.

### Características Principales

- **Autenticación**: JWT + OAuth2 con Microsoft Entra ID
- **Gestión de Solicitudes**: Estudiantes pueden crear solicitudes de asesoría
- **Panel de Asesores**: Los asesores pueden aceptar y gestionar solicitudes
- **Calendario**: Integración con Outlook Calendar
- **Chat**: Mensajería en tiempo real entre estudiantes y asesores
- **Integración Microsoft Teams**: Creación automática de reuniones

## Estructura del Proyecto

```
PeerHive/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── main.py       # Configuración principal
│   │   ├── models.py     # Modelos de datos
│   │   ├── services/     # Servicios (Teams, Calendar)
│   │   ├── application/  # Casos de uso
│   │   ├── domain/       # Entidades y repositorios
│   │   └── infrastructure/ # Adaptadores
│   ├── requirements.txt
│   └── Dockerfile
│
├── src/                  # Frontend Vanilla JS
│   ├── ui/              # Componentes de UI
│   ├── services/        # Servicios API
│   ├── store/           # Estado de la aplicación
│   ├── api/             # Configuración API
│   └── utils/           # Utilidades
│
├── docs/                 # Documentación
│   ├── DISTRIBUCION_TRABAJO_BACKEND.md
│   ├── DISTRIBUCION_TRABAJO_FRONTEND.md
│   ├── ARQUITECTURA_PEERHIVE.md
│   ├── requirements.md
│   └── ...
│
├── tests/                # Pruebas pytest
├── index.html            # Página principal
├── style.css            # Estilos
├── docker-compose.yml
└── README.md
```

## Tech Stack

| Componente | Tecnología |
|------------|------------|
| Backend | FastAPI |
| Base de Datos | MongoDB |
| Autenticación | JWT + OAuth2 (Microsoft Entra ID) |
| Frontend | Vanilla JavaScript (SPA) |
| Calendario | Microsoft Graph API |
| Reuniones | Microsoft Teams |
| Testing | pytest |
| CI/CD | GitHub Actions |

## Inicio Rápido

### Requisitos

- Python 3.11+
- Docker y Docker Compose
- MongoDB (incluido en docker-compose)
- Node.js (opcional, para desarrollo frontend)

### Instalación

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Iniciar servicios
docker-compose up -d

# 3. Acceder a la aplicación
# Frontend: http://localhost
# Backend API: http://localhost:8000
# Swagger: http://localhost:8000/docs
```

### Desarrollo Local

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (servidor estático)
# Abrir index.html en navegador o usar servidor estático
python -m http.server 8000
```

## Roles de Usuario

| Rol | Descripción |
|-----|-------------|
| **Estudiante** | Puede crear solicitudes de asesoría, chatear con asesores |
| **Asesor** | Puede aceptar solicitudes, gestionar materias, chatear con estudiantes |
| **Admin** | Acceso completo, gestión de usuarios y reportes |

## Cuentas Demo

- **Administrador**: admin@demo.com / admin
- **Asesor**: asesor@demo.com / asesor
- **Estudiante**: estudiante@demo.com / estudiante

## Documentación

La documentación detallada se encuentra en la carpeta [`docs/`](docs/):

- [`docs/DISTRIBUCION_TRABAJO_FRONTEND.md`](docs/DISTRIBUCION_TRABAJO_FRONTEND.md) - Gaps y distribución del frontend
- [`docs/DISTRIBUCION_TRABAJO_BACKEND.md`](docs/DISTRIBUCION_TRABAJO_BACKEND.md) - Distribución del backend
- [`docs/ARQUITECTURA_PEERHIVE.md`](docs/ARQUITECTURA_PEERHIVE.md) - Arquitectura del proyecto
- [`docs/requirements.md`](docs/requirements.md) - Requisitos funcionales

## API Endpoints

### Autenticación

```
GET  /api/auth/login
GET  /api/auth/callback
GET  /api/auth/logout
GET  /api/auth/me
```

### Usuarios

```
GET    /api/users
GET    /api/users/{id}
POST   /api/users
PUT    /api/users/{id}
DELETE /api/users/{id}
```

### Solicitudes

```
GET    /api/requests
GET    /api/requests/{id}
POST   /api/requests
PUT    /api/requests/{id}
DELETE /api/requests/{id}
```

### Sesiones

```
GET    /api/sessions
GET    /api/sessions/{id}
POST   /api/sessions
PUT    /api/sessions/{id}
```

### Microsoft Graph

```
GET  /calendar/events
POST /calendar/events
POST /teams/meetings
GET  /teams/meetings/{id}/attendance
```

## Contribuidores

- Equipo de desarrollo PeerHive

---

*PeerHive – Conectando estudiantes y asesores académicos*
