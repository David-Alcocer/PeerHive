# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")

REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "dev-change-me")

# Para que funcione con cuenta personal + organizacional
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["User.Read"]