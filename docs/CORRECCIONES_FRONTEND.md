# Correcciones y Pendientes del Frontend - PeerHive

## Estado: REQUIERE REVISIÓN Y CORRECCIÓN

---

## Lista de Correcciones Identificadas

### 1. Constantes de API Duplicadas

**Archivo:** [`src/api/config.js`](src/api/config.js)

**Problema:**
```javascript
export const API_URL = 'http://localhost:8000';           // Línea 2
export const API_BASE_URL = 'http://localhost:8000/api';   // Línea 3
```

**Solución:** Unificar a usar solo `API_BASE_URL`

**Asignado a:** Dev 3

---

### 2. Endpoint de Autenticación Incorrecto 

**Archivo:** [`src/services/auth.service.js`](src/services/auth.service.js)

**Línea:** 181

**Problema:**
```javascript
const response = await fetch(`${API_URL}/auth/me`, {...});
```

**Solución:**
```javascript
const response = await fetch(`${API_URL}/api/auth/me`, {...});
```

**Asignado a:** Dev 4

---

### 3. Estados en Español vs Inglés (CRÍTICO)

El backend usa estados en INGLÉS pero el frontend usa ESP:

#### 3.1 En [`src/services/request.service.js`](src/services/request.service.js)

| Línea | Actual | Cambiar a |
|-------|--------|-----------|
| 18 | `status: 'pendiente'` | `status: 'pending'` |
| 34 | `req.status !== 'pendiente'` | `req.status !== 'pending'` |
| 50 | `status: 'agendada'` | `status: 'approved'` |
| 55 | `req.status = 'agendada'` | `req.status = 'approved'` |

#### 3.2 En [`src/ui/requests.js`](src/ui/requests.js)

| Línea | Actual | Cambiar a |
|-------|--------|-----------|
| 168 | `req.status === 'pendiente'` | `req.status === 'pending'` |

**Asignado a:** Dev 4

---

### 4. Validación de isAdvisorApproved

**Archivo:** [`src/store/state.js`](src/store/state.js)

**Línea:** 50-51

**Problema:** El campo puede no existir en usuarios del backend

**Solución:** Agregar validación defensiva:
```javascript
if (u.role === 'advisor' && typeof u.isAdvisorApproved !== 'boolean') {
    u.isAdvisorApproved = u.isAdvisorApproved ?? false;
}
```

**Asignado a:** Dev 3

---

### 5. Visualización de Status en Calendario

**Archivo:** [`src/ui/calendar.js`](src/ui/calendar.js)

**Línea:** 148

**Problema:** `ses.status` se muestra sin formatear

**Solución:**
```javascript
// Cambiar de:
<span class="badge status-${ses.status}">${ses.status}</span>

// A:
<span class="badge status-${ses.status}">${ses.status.charAt(0).toUpperCase() + ses.status.slice(1)}</span>
```

**Asignado a:** Dev 4

---

##  Dudas y Preguntas Pendientes

### D1: Integración con Microsoft Graph
- ¿El backend tiene implementados los endpoints `/api/calendar/events` y `/api/teams/meetings`?
- ¿Los endpoints requieren autenticación OAuth adicional?

### D2: Estados de Solicitud Completos
- ¿Cuáles son todos los estados válidos del backend?
  - pending
  - taken
  - completed
  - cancelled
- ¿Qué estado usa cuando una sesión está "agendada" pero aún no se ha realizado?

### D3: Formato de Fechas
- ¿El backend usa ISO 8601 (`datetimeISO`) o timestamps?
- ¿Necesita timezone específico?

### D4: Modelo de Chat
- ¿El backend tiene un modelo de Chat implementado?
- ¿O es solo local storage?

### D5: Permisos de Roles
- ¿Qué endpoints de API existen para cada rol?
- ¿El admin puede hacer todo?

---

## 📁 Archivos del Frontend a Revisar

```
src/
├── api/
│   └── config.js                    # ❌ Constantes duplicadas
├── services/
│   ├── auth.service.js              # ❌ Endpoint incorrecto
│   ├── request.service.js           # ❌ Estados en español
│   ├── session.service.js           # ✅ OK
│   ├── chat.service.js              # ✅ OK
│   └── user.service.js              # ✅ OK
├── store/
│   └── state.js                     # ❌ Validación isAdvisorApproved
└── ui/
    ├── admin.js                     # ⚠️ Revisar
    ├── dashboard.js                 # ✅ OK
    ├── chat.js                     # ✅ OK
    ├── requests.js                  # ❌ Estados en español
    ├── calendar.js                  # ❌ Status sin formatear
    ├── advisor.js                   # ⚠️ Revisar
    ├── auth.js                      # ✅ OK
    ├── router.js                    # ✅ OK
    └── settings.js                  # ✅ OK
```

---

## 🎯 Prioridades de Corrección

| Prioridad | Corrección | Archivo |
|-----------|------------|---------|
| **ALTA** | Estados 'pendiente'/'agendada' → inglés | request.service.js |
| **ALTA** | Endpoint /auth/me → /api/auth/me | auth.service.js |
| **MEDIA** | Unificar constantes API | config.js |
| **MEDIA** | Formatear status en calendario | calendar.js |
| **BAJA** | Validación isAdvisorApproved | state.js |

---

## ✅ Checklist de Correcciones

- [ ] Dev 3: Unificar API_URL y API_BASE_URL
- [ ] Dev 3: Validar isAdvisorApproved en state.js
- [ ] Dev 4: Corregir endpoint /auth/me en auth.service.js
- [ ] Dev 4: Cambiar 'pendiente' a 'pending' en request.service.js
- [ ] Dev 4: Cambiar 'agendada' a 'approved' en request.service.js
- [ ] Dev 4: Cambiar 'pendiente' a 'pending' en requests.js (UI)
- [ ] Dev 4: Formatear status en calendar.js

---

## 📊 Resumen por Desarrollador

### Dev 3: Frontend Admin + Dashboard
- [ ] Unificar constantes de API (config.js)
- [ ] Validar isAdvisorApproved (state.js)
- [ ] Panel de administración completo
- [ ] Dashboard con estadísticas

### Dev 4: Frontend User (Chat, Solicitudes, Calendario)
- [ ] Corregir endpoint auth (auth.service.js)
- [ ] Corregir estados en request.service.js
- [ ] Corregir estados en requests.js UI
- [ ] Formatear status en calendar.js
- [ ] Chat con adjuntos
- [ ] Calendario con sesiones
- [ ] Solicitudes funcionales
