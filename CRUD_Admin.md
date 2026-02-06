# Documentación Técnica: Sistema de Gestión de Usuarios y Roles

## 1. Definición del Modelo de Datos (POO con Pydantic)
En Python, definiremos una clase que represente al usuario. MongoDB guardará las URLs (links) de las imágenes, no los archivos en sí.

* **Identificadores:** `id` (generado por MongoDB como `_id`) y `email` (institucional).
* **Estado de Verificación:** `is_verified` (Booleano).
* **Gestión de Roles:** `role` (Valores: `"student"`, `"tutor"`, `"admin"`).
* **Metadatos de Perfil:** `full_name`, `career`, `semester`.
* **Evidencias (URLs de imágenes):**
    * `id_card_url`: Link a la foto de la credencial (para ser usuario verificado).
    * `kardex_screenshot_url`: Link a la captura del Kardex (para validar si puede ser tutor).

---

## 2. Operaciones del CRUD (Nivel Admin)
Estas funciones vivirán en tu archivo de rutas (`routes`) y controladores en FastAPI:

* **C - Create:** Creación de la cuenta inicial del alumno o registro manual de nuevos Admins.
* **R - Read (Consulta):**
    * **Filtro de Aspirantes:** Buscar usuarios donde `role == "student"` y tengan una `kardex_screenshot_url` cargada, pero aún no sean tutores.
    * **Vista de Verificación:** El Admin obtiene el link de la imagen para abrirla y validar datos.
* **U - Update (La clave del proyecto):**
    * **Aprobación de Tutor:** El Admin cambia el `role` a `"tutor"` tras ver la captura del Kardex.
    * **Verificación de Identidad:** Cambiar `is_verified` a `true`.
* **D - Delete:** Eliminar cuentas que suban información falsa o capturas que no correspondan.

---

## 3. Integración con MongoDB (NoSQL)
Seguimos usando MongoDB por su capacidad de manejar documentos flexibles:

* **Referenciación de Archivos:** Guardamos solo el "path" (ruta) de la imagen. Esto mantiene la base de datos veloz.
* **Colección:** `users`.
* **Motor Asíncrono:** Usarás la librería `Motor` para que mientras el Admin carga una imagen pesada, el resto de la app no se congele.

---

## 4. Lógica de Seguridad y Roles
Asegurar que nadie "hacker" se convierta en Admin solo cambiando un texto:

* **Protección de Endpoints:** Usarás una función (dependencia) en FastAPI que verifique:
    > `if user.role != "admin": raise HTTPException(403)`
* **Validación de Evidencias:** El sistema solo permitirá al Admin cambiar el rol a `"tutor"` si el campo `kardex_screenshot_url` no está vacío.

---

## 5. Workflow de Verificación
Este es el paso a paso corregido para tu proyecto:

1.  **Solicitud:** El estudiante sube la captura de pantalla de su último semestre.
2.  **Almacenamiento:** El Backend guarda la imagen en una carpeta y genera un link.
3.  **Actualización DB:** Se guarda ese link en el campo `kardex_screenshot_url` del estudiante en MongoDB.
4.  **Revisión Admin:** El Admin entra a su panel, ve la lista de solicitudes, hace clic en el link y revisa que el nombre y las notas en la imagen coincidan.
5.  **Promoción:** Si todo es correcto, el Admin presiona "Aprobar" y el Backend ejecuta el Update del role a `"tutor"`.

---

## 6. Tabla de Endpoints Administrativos

| Operación CRUD | Método HTTP | Endpoint (URL) | Acción del Admin |
| :--- | :--- | :--- | :--- |
| **Read** | `GET` | `/admin/users/pending` | Ver la lista de alumnos que subieron su captura y esperan validación. |
| **Read** | `GET` | `/admin/users/{user_id}` | Ver la información detallada y la foto del Kardex de un alumno específico. |
| **Update** | `PATCH` | `/admin/users/{user_id}/verify` | El botón que presiona el Admin para poner `is_verified = True`. |
| **Update** | `PATCH` | `/admin/users/{user_id}/promote` | El botón para cambiar el rol de `student` a `tutor`. |
| **Delete** | `DELETE` | `/admin/users/{user_id}` | Expulsar o borrar a un usuario que subió una imagen falsa. |