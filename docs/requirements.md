# Proyecto PeerHive · Historias de Usuario y Requisitos No Funcionales (Actualizado Backend)

Este documento define las **Historias de Usuario (HU)** y los **Requisitos No Funcionales (RNF)** alineados específicamente con la implementación actual del **Backend de PeerHive**, considerando:

- Autenticación con Microsoft Entra ID
- Gestión de roles y sesiones
- CRUD de usuarios
- Sistema de tickets
- Chat con WebSockets
- Integración con Microsoft Graph / Teams
- Validación de asesores mediante **captura de pantalla del semestre equivalente (NO PDF)**

---

# 🧩 Historias de Usuario (Actualizadas)

| ID | Módulo | Actor | Historia de Usuario | Criterios de Aceptación | Prioridad |
|----|--------|--------|---------------------|--------------------------|-----------|
| HU-001 | Autenticación | Usuario | Como usuario quiero iniciar sesión mediante Microsoft Entra ID para validar que pertenezco a la universidad. | El backend valida token OAuth2, obtiene información desde Microsoft Graph y crea/actualiza el usuario en la base de datos. | Alta |
| HU-002 | Roles | Usuario | Como usuario quiero seleccionar si soy asesor o aprendiz para habilitar funcionalidades específicas. | El rol se guarda en base de datos y define acceso a endpoints protegidos. | Alta |
| HU-003 | Validación asesor | Usuario (Asesor) | Como aspirante a asesor quiero subir una **captura de pantalla del semestre equivalente** para validar que cumplo los requisitos académicos. | El sistema acepta imágenes (jpg/png), guarda el archivo, marca el estado como "pendiente" y requiere aprobación de admin. | Alta |
| HU-004 | Administración | Administrador | Como administrador quiero aprobar o rechazar solicitudes de asesores para controlar quién puede brindar asesorías. | El admin puede cambiar el estado a aprobado o rechazado y notificar al usuario. | Alta |
| HU-005 | Usuarios | Administrador | Como administrador quiero realizar CRUD de usuarios para gestionar cuentas dentro del sistema. | Existen endpoints protegidos para crear, consultar, actualizar y desactivar usuarios. | Alta |
| HU-006 | Tickets | Aprendiz | Como aprendiz quiero crear un ticket de asesoría especificando materia y descripción para solicitar ayuda. | El ticket se crea con estado "abierto" y queda disponible para asesores. | Alta |
| HU-007 | Tickets | Asesor | Como asesor quiero ver tickets disponibles para aceptarlos según mi disponibilidad. | El backend lista tickets filtrables por materia y estado. | Alta |
| HU-008 | Tickets | Asesor | Como asesor quiero aceptar un ticket para asignármelo. | El estado cambia a "asignado" y se bloquea para otros asesores. | Alta |
| HU-009 | Calendario | Usuario | Como usuario quiero que las sesiones aceptadas generen un evento con enlace de Microsoft Teams. | El backend genera enlace mediante Microsoft Graph y lo asocia al ticket. | Alta |
| HU-010 | Chat | Usuario | Como usuario quiero comunicarme mediante chat en tiempo real con la persona asignada al ticket. | Se habilita WebSocket únicamente cuando el ticket está asignado. | Alta |
| HU-011 | Sesiones | Sistema | Como sistema quiero controlar la sesión del usuario mediante tokens seguros. | Se valida token en cada request protegida. | Alta |
| HU-012 | Límite de solicitudes | Usuario | Como usuario quiero tener un límite de tickets activos para evitar abuso del sistema. | No se permiten más de 3 tickets activos simultáneamente por usuario. | Media |
| HU-013 | Cierre de ticket | Usuario | Como usuario quiero cerrar un ticket una vez finalizada la asesoría. | El estado cambia a "cerrado" y se registra fecha de finalización. | Media |
| HU-014 | Reportes | Administrador | Como administrador quiero visualizar reportes de soporte generados por usuarios. | Se almacenan y listan reportes con seguimiento de estado. | Media |

---

# 🧪 Requisitos No Funcionales (Actualizados Backend)

| ID | Categoría | Requisito |
|----|------------|-----------|
| RNF-001 | Seguridad | Toda autenticación debe realizarse mediante OAuth2 con validación de token JWT emitido por Microsoft Entra ID. |
| RNF-002 | Seguridad | Los endpoints protegidos deben validar rol y estado del usuario antes de permitir acceso. |
| RNF-003 | Seguridad | Las contraseñas locales (si existieran) deben almacenarse con hashing seguro (bcrypt o equivalente). |
| RNF-004 | Seguridad | Los archivos de validación (captura de semestre equivalente) deben almacenarse de forma segura y no exponerse públicamente. |
| RNF-005 | Seguridad | Las conexiones WebSocket deben requerir autenticación previa. |
| RNF-006 | Rendimiento | El tiempo de respuesta promedio de la API no debe superar 500 ms bajo carga normal. |
| RNF-007 | Escalabilidad | El sistema debe estar preparado para ejecutarse en contenedores Docker. |
| RNF-008 | Disponibilidad | El sistema debe soportar múltiples conexiones simultáneas en el chat sin degradación crítica. |
| RNF-009 | Integridad | Un ticket no puede ser aceptado por más de un asesor. |
| RNF-010 | Validación académica | El sistema debe permitir únicamente imágenes (jpg, png) como comprobante de semestre equivalente. No se aceptan archivos PDF. |
| RNF-011 | Auditoría | El backend debe registrar cambios críticos como: cambio de rol, aprobación de asesor y cierre de ticket. |
| RNF-012 | Documentación | La API debe contar con documentación automática accesible en `/docs` y `/redoc`. |
| RNF-013 | Manejo de errores | El backend debe retornar códigos HTTP estándar y mensajes claros en formato JSON. |
| RNF-014 | Backup | La base de datos debe contar con respaldo periódico configurable. |
| RNF-015 | Control de acceso | Solo administradores pueden aprobar asesores o modificar roles. |
| RNF-016 | Integración externa | La generación de enlaces de Teams debe depender de Microsoft Graph y manejar fallos externos adecuadamente. |
| RNF-017 | Límite de carga | El sistema debe limitar tamaño de archivos de validación a máximo 5 MB. |
| RNF-018 | Consistencia de datos | Las transiciones de estado de ticket deben seguir flujo controlado: abierto → asignado → cerrado. |

---

# Cambios Clave Respecto a la Versión Anterior

- Eliminado: Kardex en PDF.
- Nuevo método de validación: **Captura de pantalla del semestre equivalente**.
- Refuerzo en autenticación con Microsoft Entra ID.
- Chat implementado con WebSockets autenticados.
- Control estricto de estados de tickets.
- Integración formal con Microsoft Graph para Teams.
---

Este documento refleja la arquitectura y reglas reales implementadas en el **Backend actual de PeerHive**.