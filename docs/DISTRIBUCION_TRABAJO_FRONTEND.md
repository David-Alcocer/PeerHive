# Plan de Distribución de Trabajo - Frontend PeerHive

## Visión General del Proyecto

- **Frontend**: JavaScript Vanilla con SPA
- **Backend**: FastAPI + MongoDB con arquitectura hexagonal
- **Integraciones**: Microsoft Graph API (Teams y Outlook Calendar)
- **Características**: Autenticación JWT, Chat, Calendario, Reporting

---

## Gaps Identificados por Rol

### Gaps del Estudiante

| # | Problema | Archivo(s) Afectado(s) | Tipo |
|---|----------|------------------------|------|
| 1 | Al crear una nueva solicitud, el campo materia es un input de texto en lugar de un dropdown con todas las materias disponibles | [`index.html:364`](index.html:364) | UI/UX |
| 2 | El calendario está desplazado/descentrado y la escala no es adecuada | [`style.css:1220-1226`](style.css:1220), [`src/ui/calendar.js:26`](src/ui/calendar.js:26) | CSS/UI |
| 3 | El input de fecha/hora en tickets solo permite fecha, no hora (datetime-local) | [`index.html:372`](index.html:372) | UI |
| 4 | El apartado del chat debe estar después del calendario en la navegación | [`src/ui/router.js:30-44`](src/ui/router.js:30) | UX |
| 5 | El calendario debe mostrar las solicitudes pendientes con estado "pendiente" y las sesiones con estado "aceptado/completado" | [`src/ui/calendar.js:62-94`](src/ui/calendar.js:62) | Funcional |

### Gaps del Asesor

| # | Problema | Archivo(s) Afectado(s) | Tipo |
|---|----------|------------------------|------|
| 1 | En dashboard, los cards de resumen (solicitudes, sesiones) deben ser clicables y redirigir a sus respective apartados | [`src/ui/dashboard.js:28-42`](src/ui/dashboard.js:28) | UX |
| 2 | Al aceptar una solicitud, el sistema redirige directamente al chat; debe permanecer en tickets y mostrar un botón para ir a calendario/chat | [`src/ui/requests.js:267`](src/ui/requests.js:267) | UX |
| 3 | El calendario debe mostrar el estatus de cada asesoría y la lista de sesiones debe incluir el link de Teams | [`src/ui/calendar.js:129-158`](src/ui/calendar.js:129), [`src/ui/advisor.js:103-128`](src/ui/advisor.js:103) | UI/Funcional |
| 4 | El panel de asesor no funciona correctamente porque el estudiante no tiene lista de materias para seleccionar (Gap #1 Estudiante) | [`index.html:364`](index.html:364), [`src/ui/requests.js:38`](src/ui/requests.js:38) | Funcional |

### Gaps del Administrador

| # | Problema | Archivo(s) Afectado(s) | Tipo |
|---|----------|------------------------|------|
| 1 | Las correcciones de estudiante y asesor deberían arreglar los problemas de integración | Múltiples archivos | Integración |

---

## Distribución de Desarrolladores

| Desarrollador | Rol | Área Principal |
|---------------|-----|----------------|
| **Dev 1** | Name 1 | Frontend Estudiante (Solicitudes, Calendario, Dashboard) |
| **Dev 2** | Name 2 | Frontend Asesor (Panel Asesor, Tickets, Flujo de Aceptación) |
| **Dev 3** | Name 3 | Frontend Admin + Integración + Correcciones Globales |

---

## Desarrollador 1: Frontend Estudiante

### Responsabilidades Principales
Interfaz de estudiante: solicitudes, calendario, y dashboard.

### Archivos Asignados
- [`src/ui/requests.js`](src/ui/requests.js) - **272 líneas**
- [`src/ui/calendar.js`](src/ui/calendar.js) - **158 líneas**
- [`src/ui/dashboard.js`](src/ui/dashboard.js) - **82 líneas**
- [`index.html`](index.html) - Secciones de solicitudes y calendario
- [`style.css`](style.css) - Estilos de calendario

### Tareas Específicas

#### 1. Lista de Materias en Solicitud (CRÍTICO)
**Problema**: El campo materia en [`index.html:364`](index.html:364) es un `<input id="req-subject">` en lugar de un dropdown.

**Solución**: Cambiar a `<select id="req-subject">` con todas las materias disponibles (tomar lista del panel de asesor en [`index.html:442-581`](index.html:442)).

**Pasos**:
1. Crear array de materias en [`src/utils/helpers.js`](src/utils/helpers.js) o [`src/api/config.js`](src/api/config.js)
2. Modificar [`index.html`](index.html) línea 364 para usar `<select>`
3. En [`src/ui/requests.js`](src/ui/requests.js), usar el valor del select

#### 2. Corrección del Calendario (CRÍTICO)
**Problema**: El calendario está desplazado y con mala escala.

**Archivos**:
- [`style.css:1220-1226`](style.css:1220) - `.calendar-container`
- [`src/ui/calendar.js:26`](src/ui/calendar.js:26) - `height: '100%'`

**Solución**:
1. Cambiar `height: '100%'` a `height: 'auto'` en calendar.js
2. Ajustar CSS del `.calendar-container` para centrado adecuado
3. Verificar que `min-height` sea apropiado

#### 3. Input Fecha y Hora
**Problema**: El input `datetime-local` en [`index.html:372`](index.html:372) puede no funcionar correctamente en algunos navegadores.

**Solución**:
1. Verificar formato del input
2. Asegurar que el valor se capture correctamente en [`src/ui/requests.js:40`](src/ui/requests.js:40)
3. Validar que la fecha y hora sean futuras en [`src/ui/requests.js:48-52`](src/ui/requests.js:48)

#### 4. Orden del Chat en Navegación
**Problema**: El chat aparece antes que el calendario en el sidebar.

**Archivo**: [`src/ui/router.js:30-44`](src/ui/router.js:30)

**Solución**: Reordenar las vistas en el objeto `viewRenderers` para que calendar esté antes de chat.

#### 5. Calendario con Estados de Solicitudes
**Problema**: El calendario solo muestra sesiones, no las solicitudes pendientes.

**Archivo**: [`src/ui/calendar.js:62-94`](src/ui/calendar.js:62)

**Solución**:
1. En [`renderCalendarEvents()`](src/ui/calendar.js:62), agregar solicitudes pendientes como eventos
2. Usar color diferente para solicitudes pendientes (ej. naranja) vs sesiones confirmadas (verde)
3. Cuando se acepta una solicitud, el evento debe cambiar de estado

### Criterios de Éxito
- [ ] Dropdown de materias funcionando en solicitudes
- [ ] Calendario centrado y con escala correcta
- [ ] Input de fecha y hora funcionando
- [ ] Chat aparece después del calendario en navegación
- [ ] Calendario muestra solicitudes pendientes y sesiones confirmadas

---

## Desarrollador 2: Frontend Asesor

### Responsabilidades Principales
Interfaz de asesor: panel de asesor, flujo de aceptación de solicitudes, tickets.

### Archivos Asignados
- [`src/ui/advisor.js`](src/ui/advisor.js) - **132 líneas**
- [`src/ui/requests.js`](src/ui/requests.js) - **272 líneas**
- [`src/services/request.service.js`](src/services/request.service.js) - **194 líneas**
- [`index.html`](index.html) - Sección de panel asesor

### Tareas Específicas

#### 1. Dashboard: Cards Clicables (CRÍTICO)
**Problema**: Los cards de resumen en dashboard no son clicables.

**Archivo**: [`src/ui/dashboard.js:28-42`](src/ui/dashboard.js:28)

**Solución**:
1. Modificar el HTML de los cards para incluir `onclick` o agregar eventos
2. Redirigir a:
   - Card "Solicitudes" → `view-requests`
   - Card "Sesiones" → `view-calendar`
   - Card "Rol" → `view-settings` o `view-advisor` según rol

#### 2. Flujo de Aceptación de Solicitud (CRÍTICO)
**Problema**: Al aceptar una solicitud, el sistema redirige directamente al chat ([`requests.js:267`](src/ui/requests.js:267)).

**Solución**:
1. Eliminar `switchView('view-chat')` de [`assignRequestToAdvisor()`](src/ui/requests.js:267)
2. Mostrar mensaje de éxito manteniendo en vista actual
3. Agregar botones de acción en el mensaje o en la lista de solicitudes:
   - "Ver en Calendario" → `view-calendar`
   - "Ir al Chat" → `view-chat`

#### 3. Calendario: Estatus y Link de Teams
**Problema**: El calendario no muestra el estatus y la lista de sesiones no tiene el link de Teams.

**Archivos**:
- [`src/ui/calendar.js:129-158`](src/ui/calendar.js:129) - `renderSessionList()`
- [`src/ui/advisor.js:103-128`](src/ui/advisor.js:103) - Lista de sesiones

**Solución**:
1. En [`renderSessionList()`](src/ui/calendar.js:129), agregar badge de estatus formateado
2. Agregar enlace de Teams cuando `ses.teamsLink` exista
3. En [`advisor.js`](src/ui/advisor.js), asegurar que el link de Teams se muestre correctamente

#### 4. Panel de Asesor - Integración con Materias
**Problema**: Depende del Gap #1 de estudiante (lista de materias).

**Solución**: Una vez resuelto el Gap #1, verificar que:
1. Las materias del estudiante coincidan con las del asesor
2. Las solicitudes se filtren correctamente por materia
3. El panel de asesor muestre las materias guardadas

### Criterios de Éxito
- [ ] Cards de dashboard son clicables y redirigen correctamente
- [ ] Al aceptar solicitud, se mantiene en tickets con opciones a calendario/chat
- [ ] Calendario muestra estatus de asesoría
- [ ] Lista de sesiones incluye link de Teams
- [ ] Panel de asesor funciona con lista de materias

---

## Desarrollador 3: Frontend Admin + Integración

### Responsabilidades Principales
Panel de administración, correcciones globales de integración, consistencia de estados.

### Archivos Asignados
- [`src/ui/admin.js`](src/ui/admin.js)
- [`src/ui/settings.js`](src/ui/settings.js)
- [`src/services/user.service.js`](src/services/user.service.js)
- [`src/store/state.js`](src/store/state.js)

### Tareas Específicas

#### 1. Estados Consistentes (PENDIENTE - Revisión)
**Problema**: Hay inconsistencia en los estados entre frontend y backend.

**Archivos a verificar**:
- [`src/services/request.service.js:18`](src/services/request.service.js:18) - `'pendiente'`
- [`src/services/request.service.js:47`](src/services/request.service.js:47) - `'agendada'`
- [`src/ui/requests.js:168`](src/ui/requests.js:168) - `'pendiente'`

**Estados del Backend** (debe ser el estándar):
- `pending` - Pendiente
- `taken` - Tomada/Aceptada
- `approved` - Aprobada/Agendada
- `completed` - Completada
- `cancelled` - Cancelada

**Solución**:
1. Cambiar todos los `'pendiente'` a `'pending'`
2. Cambiar todos los `'agendada'` a `'approved'`
3. Usar constantes para los estados

#### 2. Validación de `isAdvisorApproved`
**Problema**: El campo puede no existir en usuarios del backend.

**Archivo**: [`src/store/state.js:50-51`](src/store/state.js:50)

**Solución**: Ya está manejado con la validación existente.

#### 3. Unificación de Constantes de API
**Problema**: Duplicación de `API_URL` y `API_BASE_URL`.

**Archivo**: [`src/api/config.js`](src/api/config.js)

**Solución**: Usar solo `API_BASE_URL` para todas las llamadas.

#### 4. Integración General
**Problema**: Los gaps de estudiante y asesor afectan la integración general.

**Solución**: Coordinar con Dev 1 y Dev 2 para asegurar que las correcciones no rompan la integración existente.

### Criterios de Éxito
- [ ] Estados consistentes en todo el frontend
- [ ] Constantes de API unificadas
- [ ] Validación de isAdvisorApproved funcionando
- [ ] Integración completa entre estudiante, asesor y admin

---

## Tabla de Referencia de Correcciones

| # | Área | Archivo | Problema | Solución | Asignado a |
|---|------|---------|----------|----------|-------------|
| 1 | Estudiante | index.html:364 | Input materia texto | Cambiar a select con lista de materias | Dev 1 |
| 2 | Estudiante | style.css:1220, calendar.js:26 | Calendario descentrado | Ajustar height y CSS | Dev 1 |
| 3 | Estudiante | index.html:372 | Input datetime | Verificar funcionamiento | Dev 1 |
| 4 | Estudiante | router.js:30 | Chat antes de calendario | Reordenar vistas | Dev 1 |
| 5 | Estudiante | calendar.js:62 | Solo muestra sesiones | Agregar solicitudes pendientes | Dev 1 |
| 6 | Asesor | dashboard.js:28 | Cards no clicables | Agregar onclick | Dev 2 |
| 7 | Asesor | requests.js:267 | Redirige a chat | Mantener en tickets + botones | Dev 2 |
| 8 | Asesor | calendar.js:129 | Sin estatus | Mostrar badge de estatus | Dev 2 |
| 9 | Asesor | advisor.js:103 | Sin link Teams | Mostrar teamsLink | Dev 2 |
| 10 | Admin | request.service.js:18,47 | Estados inconsistentes | Cambiar a inglés | Dev 3 |
| 11 | Admin | requests.js:168 | Estado 'pendiente' | Cambiar a 'pending' | Dev 3 |
| 12 | Admin | config.js | Constantes duplicadas | Unificar | Dev 3 |

---

## Dependencias entre Desarrolladores

```
Dev 1 (Estudiante) ─────► Dev 2 (Asesor)
        │                         │
        │                         │
        └────────► Dev 3 ◄────────┘
                      │
                      ▼
              (Integración Final)
```

### Notas:
- **Dev 1** debe completar el Gap #1 (lista de materias) para que **Dev 2** pueda completar el Gap #4 (panel de asesor)
- **Dev 3** puede trabajar en paralelo pero debe esperar a que los estados estén definidos por Dev 1 y Dev 2

---

## Archivos del Frontend (Referencia)

```
src/
├── ui/
│   ├── admin.js              # Dev 3
│   ├── advisor.js            # Dev 2
│   ├── auth.js               # Autenticación
│   ├── calendar.js           # Dev 1
│   ├── chat.js               # Chat (compartido)
│   ├── dashboard.js          # Dev 1 + Dev 2
│   ├── requests.js           # Dev 1 + Dev 2
│   ├── router.js             # Navegación
│   ├── settings.js           # Dev 3
│   └── theme.js              # Temas
├── services/
│   ├── auth.service.js       # Autenticación
│   ├── chat.service.js       # Chat
│   ├── request.service.js    # Solicitudes (Dev 3 - estados)
│   ├── session.service.js    # Sesiones
│   └── user.service.js       # Usuarios
├── store/
│   └── state.js              # Estado (Dev 3)
├── api/
│   └── config.js             # Config API (Dev 3)
├── utils/
│   └── helpers.js            # Utilidades
└── main.js                  # Entry point
```

---

## Milestones Sugeridos

### Sprint 1: Fundamentos Estudiante
- [ ] Dev 1: Dropdown de materias en solicitudes
- [ ] Dev 1: Corrección de calendario (CSS + JS)
- [ ] Dev 1: Input fecha/hora funcionando

### Sprint 2: Navegación y Calendario
- [ ] Dev 1: Orden del chat después de calendario
- [ ] Dev 1: Calendario con solicitudes + sesiones
- [ ] Dev 2: Dashboard con cards clicables

### Sprint 3: Flujo de Asesor
- [ ] Dev 2: Flujo de aceptación sin redirigir automáticamente
- [ ] Dev 2: Estatus en calendario
- [ ] Dev 2: Link de Teams en listas

### Sprint 4: Integración y Admin
- [ ] Dev 3: Estados consistentes (inglés)
- [ ] Dev 3: Constantes unificadas
- [ ] Dev 3: Integración completa

---

## Notas Adicionales

1. **Estados de Solicitud**: El backend usa estados en inglés. El frontend debe adoptar el mismo estándar para evitar problemas de integración con el API real.

2. **Lista de Materias**: La lista de materias del panel de asesor ([`index.html:442-581`](index.html:442)) debe ser la fuente verdad para el dropdown de solicitudes del estudiante.

3. **Teams Integration**: Los links de Teams se generan en [`request.service.js`](src/services/request.service.js) y se almacenan en la sesión. Asegurar que se propaguen correctamente a la UI.

4. **LocalStorage**: El estado se persiste en localStorage. Cualquier cambio en estructuras de datos debe manejar migraciones si es necesario.
