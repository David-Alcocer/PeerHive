import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_and_read_user(monkeypatch):
    # use in-memory or fake db? For now monkeypatch crud to avoid actual Mongo
    from app import crud

    async def fake_create(user_in):
        return {"_id": "507f1f77bcf86cd799439011", "email": user_in.email, "nombre": user_in.nombre, "rol": user_in.rol}

    monkeypatch.setattr(crud, "create_user", fake_create)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"email": "test@university.edu", "nombre": "Alice", "contraseña": "pwd12345", "rol": "usuario"}
        resp = await ac.post("/api/usuarios", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "test@university.edu"

