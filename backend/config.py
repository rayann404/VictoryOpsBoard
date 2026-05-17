from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent

class AuthJWT(BaseModel):
    # ПЕРЕШЛИ НА HS256: проще и надежнее для хакатона
    secret_key: str = "victory-group-super-secret-key-12345"
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"
    GEMINI_API_KEY: str = "" 
    AI_MODEL: str = "gemini-2.5-flash" 

    auth_jwt: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


settings = Settings()
