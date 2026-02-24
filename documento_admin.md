# 🚀 Documentación: Sistema de Verificación de Asesores (Módulo Admin)

Esta documentación describe la implementación del módulo administrativo para **PeerHive**, diseñado para gestionar la transición de roles de estudiantes a asesores mediante la verificación de documentos académicos (Kardex).

---

## 🏗️ 1. Arquitectura y Estructura de Archivos
El proyecto utiliza una arquitectura de microservicios contenida en **Docker**. Para que el motor de **FastAPI** localice los módulos, los archivos se organizaron en la carpeta `backend/app/`.

* **`main.py`**: Punto de entrada de la aplicación; inicializa FastAPI y conecta los routers.
* **`models.py`**: Define los moldes de datos (Clases de Pydantic/POO) y roles permitidos (`RoleEnum`).
* **`admin.py`**: Contiene la lógica de negocio y los endpoints exclusivos para el administrador.

---

## 📊 2. Definición del Modelo de Datos (POO)
Se aplicaron conceptos de Programación Orientada a Objetos para definir la estructura del usuario:

* **Roles**: Administrado mediante un `Enum` (`ADMIN`, `ADVISOR`, `STUDENT`).
* **Campos de Verificación**:
    * `kardex_screenshot_url`: Almacena la ubicación de la prueba académica.
    * `is_verified`: Booleano que controla si el usuario ya fue aprobado por un administrador.

---

## 🛠️ 3. Funcionalidades del Administrador (Endpoints)

### A. Listar Usuarios Pendientes (`GET /admin/users/pending`)
Consulta la base de datos **MongoDB** buscando usuarios que cumplan dos condiciones:
1.  Tener una URL de Kardex cargada (no nula).
2.  Tener el campo `is_verified` en `False`.

### B. Promover a Asesor (`PATCH /admin/users/{user_id}/promote`)
Acción de aprobación que realiza el administrador:
1.  **Validación**: Verifica la existencia del usuario y la presencia del documento en el perfil.
2.  **Actualización**: Cambia el rol a `advisor` y marca `is_verified` como `True`.

---

## 🔌 4. Tecnologías Utilizadas

| Tecnología | Propósito |
| :--- | :--- |
| **FastAPI** | Framework encargado de gestionar las peticiones y validaciones automáticas. |
| **Swagger UI** | Interfaz interactiva para probar el código en tiempo real (`/docs`). |
| **Docker** | Contenedor que asegura que el código funcione igual en cualquier computadora. |
| **MongoDB** | Base de datos NoSQL donde se almacena la información de los usuarios. |

---

## 💡 5. Lecciones Aprendidas (Troubleshooting)
Durante el desarrollo se resolvieron conflictos críticos de rutas en Docker:
* **Importaciones Relativas**: Se aprendió que dentro de contenedores Docker, es vital usar `from . import admin` o rutas absolutas para evitar el error `ModuleNotFoundError`.
* **Estructura de Carpetas**: La ubicación de los archivos dentro de la subcarpeta `app/` es fundamental para que el `Dockerfile` pueda mapear el volumen correctamente.

---

> **Estado del Proyecto**: Pull Request enviado y pendiente de revisión por Codeowners.