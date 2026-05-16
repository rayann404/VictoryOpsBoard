from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "core" / "security" / "private_jwt_key.pem"
    public_key_path: Path = BASE_DIR / "core" / "security" / "public_jwt_key.pem"
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

class Settings(BaseModel):
    DATABASE_URL: str


settings = Settings
