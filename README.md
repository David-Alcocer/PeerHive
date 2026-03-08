# PeerHive

## Módulo CRUD de Usuarios

El proyecto incluye un servicio FastAPI independiente que implementa el CRUD de la entidad **Usuario** utilizando MongoDB como almacén de datos. Esto servirá como pieza para un futuro montaje con otros módulos.

### Configuración y ejecución

1. Copie `.env.example` a `.env` y ajuste la URI de MongoDB si es necesario.
2. Cree un entorno virtual e instale dependencias:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
eval "$(source venv/bin/activate)"  # Unix/macOS
pip install -r requirements.txt
```

3. Inicie el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```

4. Documentación automática disponible en `http://localhost:8000/docs` o `/redoc`.

### Pruebas

Hay un conjunto básico de pruebas ubicadas en `tests/test_users.py`. Se pueden ejecutar con `pytest` después de instalar dependencias de desarrollo.

> **Administración:** Las operaciones de actualización y eliminación requieren el encabezado HTTP `X-Role: admin` para simular autorización de administrador.


