# Análisis Técnico Específico de Imperfecciones actuales en PeerHive

Profundizando en el estado actual del código y arquitectura de **PeerHive**, he detectado imperfecciones técnicas principales. Con tu última decisión estratégica para la validación de asesores, lograste simplificar enormemente la infraestructura y eliminar el peor de los problemas de seguridad.

A continuación, los retos técnicos a resolver y cómo quedará estructurado ahora que usamos **Validación por Lista Blanca Administrativa**:

## 1. Validación Amateur y Manipulable (RESUELTO ESTRATÉGICAMENTE)

**El problema técnico inicial:**
Basar la confianza académica en que un usuario suba una *"captura de pantalla del semestre equivalente"* (jpg/png), e intentar guardar esa imagen de forma persistente en servidores Docker efímeros, generaba un inmenso hueco de falsificación y pérdida de archivos con cada reinicio de servidor, obligando a rentar plataformas de terceros como AWS S3 solo para almacenar fotos.

**La Nueva Solución Implementada (Listas Blancas + Carga Segura):**
Se elimina por completo la carga de archivos o comprobantes fotográficos.
En su lugar, PeerHive opera con presunción académica cerrada:
1. **Delegación Administrativa:** "Secretaría" carga un listado `.csv` de estudiantes idóneos, o bien, agrega el correo `@alumnos.uady.mx` manualmente. 
2. **Elevación Automática:** Cuando un correo que se encuentra listado en el Backend trata de iniciar sesión a través de Microsoft Entra ID (que confirma matemáticamente la propiedad del correo), se le elevan los privilegios a su rol a "Asesor" de manera instantánea y segura.
3. *Excepciones Inteligentes:* Si el alumno olvidó enlistarse este semestre pero tiene un buen historial, el Administrador o Secretaría puede agregarlo entrando a la plataforma en cualquier momento introduciendo manualmente su dirección institucional. 

*Resultado:* Un sistema hiper-profesional, validación libre de carga administrativa doble y ya no se requieren caros servicios de infraestructura (Cloud Storage / S3).

## 2. Riesgo Crítico en Tiempo Real: WebSockets en Memoria Local

**El problema técnico:** 
Actualmente, el backend en `FastAPI` (según los estándares de implementación de WebSockets mostrados) mantiene las conexiones abiertas guardándolas en una clase o diccionario tipo `active_connections = {}` alojado únicamente en la memoria RAM del servidor de Python.

**Por qué fallará en producción:** 
Se plantea desplegar en contenedores Docker y escalar. Si el tráfico de estudiantes es alto y levantas 2 o más instancias de FastAPI (Contenedor A y Contenedor B) sucedería lo siguiente:
- El Estudiante se conecta e ingresa al **Contenedor A**.
- El Asesor inicia sesión, el balanceador de carga lo manda al **Contenedor B**.
- El Estudiante manda un mensaje ("Hola!"). El Contenedor A lo recibe, busca al Asesor en su memoria RAM local, **no lo encuentra** y la comunicación jamás se logra. 

**Corrección:**
Modificar el gestor de WebSockets de FastAPI conectándolo a un servicio llamado **Redis** (Publisher/Subscriber). Si el Contenedor A recibe un mensaje de un alumno, se lo "anuncia" en milisegundos a Redis para que repita el mensaje en el Contenedor B de forma infalible.

## 3. Inmantenibilidad y Race Conditions en el Frontend (Vanilla JS)

**El problema técnico:**
Tienen una arquitectura *Single Page Application* (SPA) armada de forma rudimentaria con Vanilla JS, manipulando directamente el Document Object Model (DOM).

**Por qué fallará en la práctica:**
1. **Pérdida del rastro durante la Autenticación:** El flujo OAuth con Microsoft requiere atrapar el Token JWT retornado en URL y compartirlo globalmente a cada petición. El Store local de Vanilla JS tenderá a re-evaluarse a ritmos dispares con la pintura (render), desincronizando la sesión de los alumnos (Race Conditions).
2. **Re-Renders Manuales del Chat:** Añadir mensajes de WebSocket de forma visual manipulando `.innerHTML` inyecta vulnerabilidades tipo XSS gravísimas, facilitando inyecciones indeseables al carecer de un sanitizado de framework en tiempo real.

**Corrección:**
Migrar de forma temprana el stack Front-End del proyecto a **React (usando Vite o Next.js)** automatiza el Virtual DOM. React Context es vital para distribuir de forma inquebrantable y segura el Token Auth a cualquier ruta protegida, minimizando cuelgues al usuario y dando un look moderno imperativo a la "Landing".
