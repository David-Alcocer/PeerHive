# 📚 PeerHive - Documentación del Proyecto

> **Versión:** 1.0  
> **Última actualización:** 2026-03-05

---

## 📋 Índice de Documentos

| Documento | Descripción |
|-----------|-------------|
| [`ARQUITECTURA_PEERHIVE.md`](ARQUITECTURA_PEERHIVE.md) | Análisis de arquitectura y propuesta de mejora |
| [`INFORME_ARQUITECTURA.md`](INFORME_ARQUITECTURA.md) | Informe de cumplimiento de arquitectura |
| [`requirements.md`](requirements.md) | Historias de usuario y requisitos funcionales |
| [`DOCUMENTACION_MS_GRAPH.md`](DOCUMENTACION_MS_GRAPH.md) | Documentación de integración con Microsoft Graph API |
| [`CHANGELOG_MS_GRAPH.md`](CHANGELOG_MS_GRAPH.md) | Historial de cambios de MS Graph |
| [`CRUD_Admin.md`](CRUD_Admin.md) | Documentación de operaciones CRUD para admin |
| [`Match_CRUDs.md`](Match_CRUDs.md) | Mapeo de operaciones CRUD |

---

## 🏗️ Arquitectura del Proyecto

PeerHive implementa una **Arquitectura Hexagonal (Ports & Adapters)** con las siguientes capas:

```
src/
├── domain/              # Entidades del negocio
├── application/         # Casos de uso
├── infrastructure/      # Adaptadores (MongoDB, MS Graph)
└── api/                # Endpoints REST
```

### Nivel de Cumplimiento: **85%**

El proyecto ha resuelto el **100% de los problemas críticos** de seguridad identificados:

- ✅ Secrets hardcodeados
- ✅ Credenciales en frontend
- ✅ Base de datos en memoria
- ✅ MongoDB sin autenticación
- ✅ Auth simulada en frontend

---

## 🚀 Inicio Rápido

### Requisitos

- Python 3.11+
- Docker y Docker Compose
- MongoDB (incluido en docker-compose)

### Instalación

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Iniciar servicios
docker-compose up -d

# 3. Ejecutar tests
pytest tests/ -v
```

---

## 📁 Estructura del Proyecto

```
PeerHive/
├── backend/           # API FastAPI
│   └── app/
│       ├── domain/    # Entidades y repositorios
│       ├── application/ # Casos de uso
│       └── infrastructure/ # Adaptadores
├── src/              # Frontend Vanilla JS
├── tests/            # Pruebas pytest
├── docs/             # Documentación
└── docker-compose.yml
```

---

## 🔧 Tech Stack

| Componente | Tecnología |
|------------|------------|
| Backend | FastAPI |
| Base de Datos | MongoDB |
| Autenticación | JWT + OAuth2 (Microsoft Entra ID) |
| Frontend | Vanilla JavaScript |
| Testing | pytest |
| CI/CD | GitHub Actions |

---

## 📞 Soporte

Para preguntas o contribuciones, favor de contactar al equipo de desarrollo.
