from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

UPLOAD_DIR = 'uploads'

class DBSettings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///./db.sqlite3"
    echo: bool = True

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR/"certs"/"jwt-private.pem"
    public_key_path: Path = BASE_DIR/"certs"/"jwt-public.pem"
    algorithm: str = "RS256"

class Settings(BaseSettings):
    db: DBSettings = DBSettings()

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()