# PeerHive - Sistema de Asesorías Académicas

Sistema web para la gestión de asesorías entre pares (estudiantes y asesores), utilizando una arquitectura moderna contenerizada.

## Stack Tecnológico

*   **Frontend:** Vanilla JavaScript (ES6 Modules) + CSS + HTML5. Servido con Nginx.
*   **Backend:** Python 3.11 + FastAPI.
*   **Base de Datos:** MongoDB.
*   **Infraestructura:** Docker & Docker Compose.

## Requisitos Previos

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo.
*   Git.

## Guía de Ejecución Rápida

Para levantar todo el entorno de desarrollo (Frontend, Backend y Base de Datos) en un solo paso:

1.  **Construir y levantar contenedores:**
    Abre una terminal en la carpeta raíz del proyecto y ejecuta:

    ```bash
    docker-compose up --build
    ```

    *La primera vez tomará unos minutos mientras descarga las imágenes y compila.*

2.  **Verificar Servicios:**
    Una vez que veas logs de "Uvicorn running..." y "Listening on...", puedes acceder a:

    *   **Frontend (App):** [http://localhost:3000](http://localhost:3000)
    *   **Backend (API):** [http://localhost:8000](http://localhost:8000)
    *   **Documentación API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **Mongo Express (Si se habilita):** Puerto 8081 (opcional).

## Estructura del Proyecto

```
.
├── backend/                # Código fuente del Backend (Python)
│   ├── app/
│   │   ├── main.py         # Punto de entrada y configuración
│   │   ├── models.py       # Modelos Pydantic (Esquema BD)
│   │   └── routes/         # (Próximamente) Endpoints
│   ├── Dockerfile          # Configuración de imagen Backend
│   └── requirements.txt    # Dependencias Python
│
├── src/                    # Código fuente del Frontend (JS)
│   ├── services/           # Lógica de negocio
│   ├── ui/                 # Componentes de interfaz
│   ├── store/              # Estado global
│   └── api/                # Cliente HTTP y Config
│
├── index.html              # Entry point Frontend
├── docker-compose.yml      # Orquestador de servicios
└── frontend.Dockerfile     # Configuración de imagen Frontend
```

## Solución de Problemas Comunes

*   **Puerto Ocupado:** Si el puerto 3000 u 8000 están en uso, edita el archivo `docker-compose.yml` y cambia el mapeo de puertos (ej: `"3001:80"`).
*   **Error de Conexión DB:** Asegúrate de que el contenedor `peerhive_mongo` esté corriendo (`docker ps`). El backend espera conectarse a `mongodb://mongo:27017`.

## Próximos Pasos (Para el Equipo)

Revisar el archivo `task.md` para ver el plan de trabajo de los Sprints de desarrollo pendiente.
