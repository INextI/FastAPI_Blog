from pydantic_settings import BaseSettings

UPLOAD_DIR = 'uploads'

class DBSettings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///./db.sqlite3"
    echo: bool = True

class Settings(BaseSettings):
    db: DBSettings = DBSettings()

settings = Settings()