# Puntos Clave del Sistema Integrado

* **Identidad Única:** El usuario se registra con un Email institucional único y una contraseña encriptada.
* **Modelo Documental:** Se utilizará **MongoDB**, por lo que el ID será un `ObjectId` generado por la base de datos, aunque se maneje como texto en el código para facilitar el CRUD.
* **Estados de Verificación:** El documento nace con `is_verified: false` y el rol inicial de usuario (o `student`).
* **Evidencias de Registro:** El usuario sube la captura de su SICEI/Kardex, cuya URL se guarda en el documento para que el Admin la revise.
* **Jerarquía de Roles:** El sistema soporta el cambio dinámico de roles (**Estudiante ↔ Asesor/Tutor**) mediante operaciones de Update autorizadas solo por Admins.
* **Formato de Comunicación:** Toda la API intercambiará datos exclusivamente en formato **JSON**.

---

## Ejemplo de JSON: El "Molde Único"
Este es el objeto que viviría en su base de datos MongoDB. Contiene tanto los campos para el registro como los necesarios para la validación de asesores.

```json
{
  "_id": "67a4e8f2b1d3e4567890abcd",
  "nombre": "David Misael Alcocer Castilla",
  "email": "david.alcocer@uady.mx",
  "password": "$2b$12$K7v8...hash_encriptado...",
  "rol": "student",
  "is_verified": false,
  "perfil": {
    "carrera": "Ingeniería de Software",
    "semestre": 2,
    "evidencias": {
      "id_card_url": "[https://peerhive.storage/fotos/id_david.jpg](https://peerhive.storage/fotos/id_david.jpg)",
      "kardex_screenshot_url": "[https://peerhive.storage/fotos/kardex_david_2026.png](https://peerhive.storage/fotos/kardex_david_2026.png)"
    }
  },
  "fecha_registro": "2026-02-06T09:32:00Z"
}