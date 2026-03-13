# Plan de Distribución de Trabajo - PeerHive

## Visión General del Proyecto


- **Backend**: FastAPI + MongoDB con arquitectura hexagonal
- **Frontend**: JavaScript Vanilla con SPA
- **Integraciones**: Microsoft Graph API (Teams y Outlook Calendar)
- **Características**: Autenticación JWT, Chat, Calendario, Reporting

---

## Distribución de Desarrolladores

| Desarrollador | Rol | Área Principal |
|---------------|-----|----------------|
| **Dev 1** | Name 1 | Integración Microsoft Graph (Teams + Calendar) |
| **Dev 2** | Name 2 | Autenticación y Seguridad + Core Backend |
| **Dev 3** | Name 3 | Frontend Admin + Dashboard |
| **Dev 4** | Name 4 | Frontend User (Chat, Solicitudes, Calendario) |
| **Dev 5** | Name 5 | Testing, CI/CD, Documentación |

---

## Desarrollador 1: Integración Microsoft Graph (CRÍTICO)

### Responsabilidades Principales
Implementación y mantenimiento de la integración con Microsoft 365 para reuniones y calendario.

### Archivos Asignados
- [`backend/app/services/teams.py`](backend/app/services/teams.py) - **368 líneas**
- [`backend/app/services/calendar.py`](backend/app/services/calendar.py) - **355 líneas**
- [`docs/DOCUMENTACION_MS_GRAPH.md`](docs/DOCUMENTACION_MS_GRAPH.md)
- [`docs/CHANGELOG_MS_GRAPH.md`](docs/CHANGELOG_MS_GRAPH.md)

### Tareas Específicas
1. **Teams Meeting Service**
   - Crear reuniones de Teams automáticas
   - Obtener reportes de asistencia
   - Gestionar participantes
   - Manejar enlaces de reuniones

2. **Calendar Service**
   - Sincronizar eventos con Outlook
   - Crear/actualizar/eliminar eventos
   - Manejar asistentes
   - Integración con reuniones online

3. **Token Management**
   - Refresh tokens de Microsoft
   - Manejo de permisos OAuth
   - Manejo de errores de API

### Criterios de Éxito
- [ ] Reuniones de Teams creadas automáticamente al aprobar sesión
- [ ] Reporte de asistencia obtenido y almacenado
- [ ] Calendario sincronizado bidireccionalmente
- [ ] Manejo robusto de errores de API

---

## Desarrollador 2: Autenticación y Seguridad + Core Backend (CRÍTICO)

### Responsabilidades Principales
Sistema de autenticación robusto, seguridad y arquitectura core del backend.

### Archivos Asignados
- [`backend/app/main.py`](backend/app/main.py) - **~600 líneas** (completo)
- [`backend/app/models.py`](backend/app/models.py) - **147 líneas**
- [`backend/app/infrastructure/repositories/`](backend/app/infrastructure/repositories/) - Todos
- [`backend/app/domain/`](backend/app/domain/) - Entidades y repositorios

### Tareas Específicas
1. **Sistema de Autenticación**
   - JWT tokens con refresh
   - Cifrado de tokens (Fernet)
   - Password hashing (bcrypt)
   - OAuth con Microsoft

2. **Core Backend**
   - Modelos Pydantic completos
   - Repositorios MongoDB
   - Use Cases (CreateRequest, AssignRequest, etc.)
   - Container DI

3. **API Endpoints**
   - CRUD completo de entidades
   - Validación de datos
   - Manejo de errores
   - Rate limiting

### Criterios de Éxito
- [ ] Autenticación JWT funcionando
- [ ] Tokens cifrados correctamente
- [ ] CRUD completo de usuarios, solicitudes, sesiones
- [ ] Repositorios implementados correctamente

---

## Desarrollador 3: Frontend Admin + Dashboard

### Responsabilidades Principales
Interfaz de administración y panel de control para administradores.

### Archivos Asignados
- [`src/ui/admin.js`](src/ui/admin.js) - **157 líneas**
- [`src/ui/dashboard.js`](src/ui/dashboard.js) - **~80 líneas**
- [`src/services/user.service.js`](src/services/user.service.js)
- [`src/ui/settings.js`](src/ui/settings.js)

### Tareas Específicas
1. **Panel de Administración**
   - Lista de usuarios con búsqueda
   - Gestión de roles (admin, advisor, student)
   - Aprobar/rechazar solicitudes de asesores
   - Estadísticas del sistema

2. **Dashboard**
   - Métricas generales
   - Actividad reciente
   - Gráficos de uso

3. **Configuración**
   - Perfil de usuario
   - Configuraciones de tema
   - Preferencias

### Tareas de Corrección (OBLIGATORIAS)

#### 1. Unificar constantes de API en [`src/api/config.js`](src/api/config.js)
- Eliminar duplicación de `API_URL` y `API_BASE_URL`
- Usar solo `API_BASE_URL` para todas las llamadas

#### 2. Validación de `isAdvisorApproved` en [`src/store/state.js`](src/store/state.js)
- Línea 50-51: El campo puede no existir en usuarios del backend
- Asegurar que la validación funcione correctamente

#### 3. Estados en [`src/ui/requests.js`](src/ui/requests.js)
- Línea 168: Cambiar `'pendiente'` a `'pending'`

### Criterios de Éxito
- [ ] CRUD de usuarios desde UI admin
- [ ] Cambio de roles funcional
- [ ] Dashboard con estadísticas en tiempo real
- [ ] **CORREGIDO**: Constantes de API unificadas
- [ ] **CORREGIDO**: Estados consistentes con backend (inglés)

---

## Desarrollador 4: Frontend User (Chat, Solicitudes, Calendario)

### Responsabilidades Principales
Interfaz de usuario para estudiantes y asesores: solicitudes, chat y calendario.

### Archivos Asignados
- [`src/ui/chat.js`](src/ui/chat.js) - **176 líneas**
- [`src/ui/requests.js`](src/ui/requests.js) - **272 líneas**
- [`src/ui/calendar.js`](src/ui/calendar.js) - **158 líneas**
- [`src/ui/advisor.js`](src/ui/advisor.js) - **~150 líneas**
- [`src/services/chat.service.js`](src/services/chat.service.js)
- [`src/services/request.service.js`](src/services/request.service.js)
- [`src/services/session.service.js`](src/services/session.service.js)
- [`src/services/auth.service.js`](src/services/auth.service.js)

### Tareas Específicas
1. **Sistema de Solicitudes**
   - Crear solicitudes de asesoría
   - Ver historial de solicitudes
   - Estados (pending, taken, completed)
   - Asignación de asesores

2. **Chat**
   - Mensajería en tiempo real (polling)
   - Adjuntos de archivos
   - Notificaciones
   - Historial de conversaciones

3. **Calendario**
   - Visualización de sesiones
   - Vista de agenda
   - Detalles de sesiones

### Tareas de Corrección (OBLIGATORIAS)

#### 1. Corrección de Estados en [`src/services/request.service.js`](src/services/request.service.js)
| Línea | Cambiar de | A |
|-------|-----------|---|
| 18 | `status: 'pendiente'` | `status: 'pending'` |
| 34 | `req.status !== 'pendiente'` | `req.status !== 'pending'` |
| 47 | `status: 'agendada'` | `status: 'approved'` |
| 55 | `req.status = 'agendada'` | `req.status = 'approved'` |

#### 2. Corrección de endpoint en [`src/services/auth.service.js`](src/services/auth.service.js)
- Línea 181: `${API_URL}/auth/me` → `${API_URL}/api/auth/me`

#### 3. Corrección de visualización en [`src/ui/calendar.js`](src/ui/calendar.js)
- Línea 148: Agregar formateo de status

### Correcciones Necesarias (CRÍTICO)
1. **Corrección de endpoints en auth.service.js**
   - Línea 181: `checkGraphAuthStatus()` usa `${API_URL}/auth/me` 
   - Debe usar `${API_URL}/api/auth/me` para consistencia

2. **Estados de solicitud**
   - En [`src/ui/requests.js`](src/ui/requests.js): Cambiar `'pendiente'` a `'pending'` (línea 168)
   - Usar constantes del enum del backend: `RequestStatusEnum.PENDING`, `.TAKEN`, `.COMPLETED`

3. **Visualización de estados en calendario**
   - En [`src/ui/calendar.js`](src/ui/calendar.js) línea 148: `ses.status` se muestra sin formatear
   - Agregar función de formateo: `status.charAt(0).toUpperCase() + status.slice(1)`

4. **Integración con Microsoft Graph**
   - Verificar que [`RequestService.createTeamsMeeting()`](src/services/request.service.js) funcione
   - Verificar que [`RequestService.createCalendarEvent()`](src/services/request.service.js) funcione

### Criterios de Éxito
- [ ] Creación de solicitudes funcional
- [ ] Chat con adjuntos funcionando
- [ ] Calendario mostrando sesiones correctamente
- [ ] Vista de asesor con solicitudes disponibles
- [ ] **CORREGIDO**: Estados en request.service.js (pendiente→pending, agendada→approved)
- [ ] **CORREGIDO**: Endpoint de autenticación Graph en auth.service.js
- [ ] **CORREGIDO**: Visualización de status en calendar.js

---

## Desarrollador 5: Testing, CI/CD y Documentación

### Responsabilidades Principales
Aseguramiento de calidad, infraestructura y documentación del proyecto.

### Archivos Asignados
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml)
- [`tests/`](tests/) - Directorio completo
- [`pytest.ini`](pytest.ini)
- [`docs/`](docs/) - Documentación
- [`docker-compose.yml`](docker-compose.yml)

### Tareas Específicas
1. **Testing**
   - Unit tests para use cases
   - Tests de integración de API
   - Tests de repositorios
   - Coverage > 70%

2. **CI/CD**
   - GitHub Actions workflow
   - Linting (Black, Flake8)
   - Tests automatizados
   - Build de Docker

3. **Documentación**
   - README.md actualizado
   - Documentación de arquitectura
   - Documentación de API
   - Guías de contribución

4. **Infraestructura**
   - Docker Compose
   - Dockerfiles
   - Variables de entorno

### Criterios de Éxito
- [ ] Pipeline CI/CD funcionando
- [ ] Tests pasando en CI
- [ ] Documentación completa
- [ ] Docker compose funcional

---

## Dependencias entre Desarrolladores

```
Dev 1 (MS Graph) ─────► Dev 2 (Auth) ─────► Dev 3 (Admin UI)
       │                      │                     │
       │                      │                     ▼
       │                      │              Dev 4 (User UI)
       │                      │
       └──────────────────────┴────► Dev 5 (Testing/CI/CD)
```

### Notas:
- **Dev 1** debe completar su trabajo primero para que **Dev 2** pueda integrar la autenticación OAuth
- **Dev 2** debe terminar el core backend antes de que **Dev 3** y **Dev 4** puedan conectar el frontend
- **Dev 5** puede trabajar en paralelo en infraestructura y testing

---

## Milestones Sugeridos

### Sprint 1: Fundamentos
- [ ] Dev 2: Autenticación básica
- [ ] Dev 1: Cliente MS Graph básico
- [ ] Dev 5: CI/CD inicial
- [ ] **CORREGIDO**: GitHub Actions workflow (actions/checkout@v4)

### Sprint 2: Core Backend
- [ ] Dev 2: CRUD completo
- [ ] Dev 1: Teams Calendar service
- [ ] Dev 5: Tests básicos

### Sprint 3: Frontend
- [ ] Dev 3: Admin panel
- [ ] Dev 4: User UI

### Sprint 4: Integración
- [ ] Dev 1 + Dev 2: Integración completa
- [ ] Dev 3 + Dev 4: UI completa
- [ ] Dev 5: Testing coverage

---

## Resumen de Correcciones del Frontend Identificadas

> **NOTA**: Las correcciones ya están asignadas a Dev 3 y Dev 4 en sus secciones respectivas.
> Esta tabla es solo para referencia rápida.

### Tabla de Referencia Rápida
| Área | Archivo | Problema | Asignado a |
|------|---------|----------|------------|
| API | config.js | Constantes duplicadas | Dev 3 |
| API | auth.service.js | Endpoint incorrecto | Dev 4 |
| Estados | request.service.js | 'pendiente'/'agendada' | Dev 4 |
| Estados | requests.js UI | 'pendiente' | Dev 3 |
| Estados | calendar.js UI | Status sin formatear | Dev 4 |
| Validación | state.js | isAdvisorApproved | Dev 3 |

---

---

## Archivos del Proyecto (Referencia)

```
PeerHive/
├── backend/
│   ├── app/
│   │   ├── main.py              # Dev 2
│   │   ├── models.py            # Dev 2
│   │   ├── services/
│   │   │   ├── teams.py         # Dev 1
│   │   │   └── calendar.py     # Dev 1
│   │   ├── application/         # Dev 2
│   │   ├── domain/              # Dev 2
│   │   └── infrastructure/     # Dev 2
│   ├── requirements.txt
│   └── Dockerfile
├── src/
│   ├── ui/
│   │   ├── admin.js             # Dev 3
│   │   ├── dashboard.js         # Dev 3
│   │   ├── chat.js              # Dev 4
│   │   ├── requests.js          # Dev 4
│   │   ├── calendar.js          # Dev 4
│   │   └── advisor.js           # Dev 4
│   ├── services/                # Dev 3 + Dev 4
│   └── store/                   # Dev 3 + Dev 4
├── tests/                      # Dev 5
├── docs/                       # Dev 5
├── .github/workflows/ci.yml    # Dev 5
└── docker-compose.yml          # Dev 5
```
