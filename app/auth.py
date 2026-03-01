import logging
import msal
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from .config import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AUTHORITY, REDIRECT_URI, SCOPES, encrypt_token
from urllib.parse import quote

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

def build_msal_app():
    return msal.ConfidentialClientApplication(
        client_id=AZURE_CLIENT_ID,
        client_credential=AZURE_CLIENT_SECRET,
        authority=AUTHORITY,
    )
@router.get("/login")
async def login(request: Request):
    request.session.clear()

    msal_app = build_msal_app()
    flow = msal_app.initiate_auth_code_flow(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        prompt="login",  #  fuerza a pedir credenciales
    )

    request.session["auth_flow"] = flow
    return RedirectResponse(flow["auth_uri"])


@router.get("/callback")
async def callback(request: Request):
    flow = request.session.get("auth_flow")
    if not flow:
        raise HTTPException(status_code=400, detail="No auth flow. Ve a /auth/login otra vez.")

    msal_app = build_msal_app()
    try:
        result = msal_app.acquire_token_by_auth_code_flow(flow, dict(request.query_params))
    except ValueError:
        raise HTTPException(status_code=400, detail="State/CSRF validation failed.")

    if "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error_description", result["error"]))

    claims = result.get("id_token_claims") or {}
    request.session["user"] = {
        "name": claims.get("name"),
        "email": claims.get("preferred_username") or claims.get("email"),
        "tid": claims.get("tid"),
        "oid": claims.get("oid"),
    }
    # Guardar el access_token de Microsoft Graph cifrado para uso en servicios
    access_token = result.get("access_token")
    if access_token:
        try:
            request.session["ms_graph_token"] = encrypt_token(access_token)
        except Exception as e:
            logger.error(f"Error cifrando access_token de Graph: {e}")
            # Continuar sin token cifrado — las funciones de Graph no estarán disponibles
            # pero el login básico sigue funcionando.
    return RedirectResponse("/app")

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()

    post_logout_redirect = "http://localhost:8000/"
    microsoft_logout = (
        "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={quote(post_logout_redirect)}"
    )

    resp = RedirectResponse(microsoft_logout, status_code=302)
    resp.delete_cookie("session")  # cookie de SessionMiddleware
    return resp