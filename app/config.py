import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESIDENTS_FILE = DATA_DIR / "residents.json"
AUDIO_DIR = DATA_DIR / "audio"

class Settings:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.residents_file = RESIDENTS_FILE
        self.audio_dir = AUDIO_DIR

        # Auth / session configuration
        self.secret_key = os.getenv("SECRET_KEY", "dev-insecure-secret-change-me")
        self.token_ttl_minutes = int(os.getenv("TOKEN_TTL_MINUTES", "20"))
        self.generic_password = os.getenv("GENERIC_PASSWORD", "ChangeMe123!")
        self.auth_cookie_name = os.getenv("AUTH_COOKIE_NAME", "access_token")
        # Secure cookies should be enabled in production (HTTPS); off for local dev.
        self.cookie_secure = os.getenv("COOKIE_SECURE", "false").lower() == "true"
        self.cookie_samesite = os.getenv("COOKIE_SAMESITE", "lax")

    def ensure_data_paths(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)

settings = Settings()
