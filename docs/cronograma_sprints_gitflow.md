# Cronograma de Sprints y Git Flow (Equipo de 6 Personas)

Dado el paradigma de trabajo con **GitHub Projects Automático**, **Git Flow** y la necesidad de evitar choques en el código, el trabajo se segmenta en **3 Sprints Semanales** con *Tickets* atados a la infraestructura técnica que no colisionan.

---

## 🛠️ Protocolo de Trabajo: Git Flow Dinámico + GitHub Projects Automatizado

Para asegurar el control del código y transparencia en las asignaciones de todos, se deberá seguir rigurosamente este flujo:
1. **Ticket al tablero automático:** Todas estas tareas (issues) deben crearse en GitHub. El tablero 'Projects' debe estar en modo Automático (To Do -> In Progress -> Done).
2. **Asignación (Assignees):** Asegúrate de auto-asignarte (solo 1 desarrollador(a) por ticket).
3. **Paso a In Progress:** Mueve libremente el ticket al empezar.
4. **Creación de ramas Git Flow cruzado:** Crea ramas locales utilizando la convención estándar donde indicas el tipo y el id del issue vinculado para que en los commits de GitHub cierre el issue de manera inteligente.
   - **Ejemplo:** `git checkout -b feature/issue-102-microsoft-login`
5. **Realización de PR (Pull Request):** Ningún desarrollador comitea directo a `main` ni `develop`. Al terminar, creas un **Pull Request (PR)** hacia la rama principal de desarrollo y añades el flag "Resolves #102" en la descripción para que GitHub mueva el Issue mágicamente a *Done*.

---

## 🚀 Cronograma por Sprints

### 🏁 SPRINT 1: Cimentación Front-End y Base Administrativa (Semana 1)
*Objetivo:* Tener funcional el Auth institucional, el esqueleto del frontend, y la infraestructura de Listas Blancas Backend lista para aceptar correos pre-autorizados.
* **[#1] [Persona 1 | F-End]** Setup inicial de Boilerplate (React/Vite). Configuración de estructura de carpetas modular (`/components`, `/hooks`, `/services`) e integración de UI Tailwind CSS.
* **[#2] [Persona 2 | F-End]** Integración de flujo OAuth2 Frontend. Captura segura del Token emitido por backend `/callback`, redirecciones del Router y creación del *Auth Context Provider*.
* **[#3] [Persona 3 | F-End]** Creación visual de la "Landing Page", y el diseño Maestro de Layout y el *Sidebar* genérico.
* **[#4] [Persona 4 | B-End]** Diseño y creación de Colección `AdvisorsWhitelist` en MongoDB. Lógica que intercepta un nuevo usuario creado vía OAuth y verifica en microsegundos si su email institucional reside en la Colección. Si reside, asignar Rol="Advisor", en lugar de "Student".
* **[#5] [Persona 5 | B-End/Admin]** Endpoint Admin: Desarrollar rutas de creación en lotes, permitiendo recibir una lista JSON o arreglo masivo de correos vía API y endpoint simple con su CRUD para permitirle a Secretaría agregar manualmente correos únicos en cualquier momento de manera individual.
* **[#6] [Persona 6 | DevOps/DB]** Orquestación inicial para desarrollo con *Docker Compose*. Levantar bases de datos motor en conjunto e integración de tests de entorno base para todo el equipo antes de programar y evitar dolores de "a mí me corre el backend y a ti no".

---

### 🚄 SPRINT 2: Funciones Administrativas (UI) y Flujo Logístico (Semana 2)
*Objetivo:* Secretaría y Asesores validan el ciclo de vida base del Ticket, logrando calendarizar exitosamente vía Teams.
* **[#7] [Persona 1 | B-End]** Re-Ajustes del `models.py` y rutas de Tickets: Integrar candados de concurrencia de base de datos para evitar que 2 Asesores intenten asignar un Ticket al mismo segundo y generen doble empalme.
* **[#8] [Persona 2 | B-End]** Lógica de Eventos Síncrona. Endpoint de crear ticket que hace la ronda asíncrona hacia Microsoft Teams API (`calendar.py`) para fijar sesión y conseguir Links.
* **[#9] [Persona 3 | F-End/Admin]** Panel Visual de *Secretaría*: Consumir endpoints del [#5]. Crear visual de tabla donde un administrador inserte dinámicamente nuevos correos de UADY en la WhiteList para autorizar manualidades tardías o errores de carga desde el Dashboard.  
* **[#10] [Persona 4 | F-End]** Flujo Visual Estudiantil: Formularios limpios de creación de tickets y lista donde el estudiante valida si el asesor ya tomó su ticket o está en estado `Pendiente`.
* **[#11] [Persona 5 | F-End]** Flujo Inteligente de Asesorías: Componente visual de cartas (Ticket Cards) para el Asesor donde elija aceptar, y pueda desplegable en modal con los datos de Teams adjuntos post-aceptación. 
* **[#12] [Persona 6 | QA/Tester]** Tests de Integración End-to-End simulados con automatización: Validando Login -> Ingresando correo bloqueado vs un correo en WhiteList, probando la lógica del nuevo modelo por separado sin intervenir la BD productiva.

---

### 💥 SPRINT 3: Mensajería de Tickets en Vivo y Estabilización (Semana 3)
*Objetivo:* Garantizar la comunicación en vivo paralela y segura mediante WebSockets robustos, evitando inestabilidad por el render manual del antiguo SPA.
* **[#13] [Persona 1 | F-End]** Panel de Diálogo Interno. Render seguro y virtualizado de las Burbujas de Chat a través de Componentes React eficientes, previendo ataques de XSS (Cross Site Scripting).
* **[#14] [Persona 2 | F-End]** Vinculación Persistente al Ticket de conexión WebSocket con el servidor del Backend reaccionando frente a una desconexión y estatus global.
* **[#15] [Persona 3 | B-End/Ops]** Desvincular de capa base asíncrona los WebSockets en `FastAPI` y enlazar a Message Broker dedicado (Redis Pub/Sub) para sostener concurrencia alta de chats proveniente de varios procesos distribuidos. 
* **[#16] [Persona 4 | B-End]** Reglas de Seguridad en Socket enrutado: Verificar JWT de estudiante/asesor antes de abrir Socket, y rechazar socket persistente si ticket pasa a estatus Finalizado/Cerrado. Validando el token cifrado del Session Middleware.
* **[#17] [Persona 5 | F-End]** Límites de Protección Operacional (Vistas): Rebotar inputs de formulario "Límite de Tickets" bloqueando UI si el Backend despacha *Limit Reached* (Max 3 Tickets localizados).
* **[#18] [Persona 6 | DevOps/Lead]** Integración Continua (CI): Workflow de GitHub Action en Pull Requests asegurando "Lint" en Python, uniendo los contenedores Front+Back+Redis y despliegue del empaquetado como Release Candidate RC-1 UADY en servidor remoto.
