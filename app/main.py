
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .config import SESSION_SECRET_KEY
from .auth import router as auth_router
from .asesorias import router as asesorias_router
app = FastAPI(
    title="PeerHive API",
    description="Sistema de asesorías con autenticación Microsoft Entra",
    version="1.0.0",
    contact={
        "name": "Freddie Uitzil",
        "email": "a24216341@alumnos.uady.mx",
    }
)
templates = Jinja2Templates(directory="templates")


app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,
    session_cookie="peerhive_session",  # nombre explícito
)

app.include_router(auth_router)
app.include_router(asesorias_router)

@app.get("/")
def root():
    return {"ok": True}

@app.get("/app", response_class=HTMLResponse)
def protected(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/auth/login")

    return templates.TemplateResponse("app.html", {
        "request": request,
        "name": user.get("name"),
        "email": user.get("email"),
    })
@app.get("/api/me")
def me(request: Request):
    return {"user": request.session.get("user")}

