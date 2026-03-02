# app/config.py
import os
import logging
from dotenv import load_dotenv
import base64
import hashlib
from cryptography.fernet import Fernet

load_dotenv()

logger = logging.getLogger(__name__)

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")

REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "dev-change-me")

# ── Clave de cifrado para tokens ──────────────────────────────────
# IMPORTANTE: La derivación de clave DEBE ser idéntica a la de backend/app/main.py
# para que los tokens cifrados aquí puedan ser descifrados por el backend.
#
# Prioridad:
#   1. TOKEN_ENCRYPTION_KEY_RAW  (variable dedicada, recomendada en producción)
#   2. SESSION_SECRET_KEY        (fallback, menos seguro — default "dev-change-me")
_token_key_source = os.getenv("TOKEN_ENCRYPTION_KEY_RAW") or SESSION_SECRET_KEY
TOKEN_ENCRYPTION_KEY = base64.urlsafe_b64encode(
    hashlib.sha256(_token_key_source.encode()).digest()
)

# Instancia singleton de Fernet
_fernet = Fernet(TOKEN_ENCRYPTION_KEY)

# Para que funcione con cuenta personal + organizacional
AUTHORITY = "https://login.microsoftonline.com/common"
# Scopes de Microsoft Graph para integración con Office 365
SCOPES = [
    "User.Read",
    "Calendars.ReadWrite",
    "OnlineMeetings.ReadWrite",
    "OnlineMeetingArtifact.Read.All",
]


# Funciones de cifrado para tokens
def encrypt_token(token: str) -> str:
    """Cifra un token usando la clave de cifrado (Fernet)."""
    return _fernet.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    """Descifra un token cifrado (Fernet)."""
    return _fernet.decrypt(encrypted_token.encode()).decode()
