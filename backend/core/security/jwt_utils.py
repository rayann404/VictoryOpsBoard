import datetime
import jwt
from config import settings
from datetime import timedelta
from modules.identity.schemas.auth_schemas import UserLoginRequest
from modules.identity.schemas.user_schemas import UserCreate

TOKEN_TYPE_FIELD = "type"
TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

def encode_jwt(
        payload: dict,
        secret: str = settings.auth_jwt.secret_key,
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    
    to_encode.update(
        exp=expire,
        iat=now,
    )
    # Используем симметричный ключ (строку)
    encoded = jwt.encode(
        to_encode,
        secret,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        secret: str = settings.auth_jwt.secret_key,
        algorithm: str = settings.auth_jwt.algorithm,
):
    # Используем симметричный ключ
    decoded = jwt.decode(
        token,
        secret,
        algorithms=[algorithm]
    )
    return decoded


def create_jwt(
        token_type: str,
        token_data: dict,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(schema: UserLoginRequest | UserCreate) -> str:
    jwt_payload = {
        "sub": schema.email,
        "email": schema.email,
    }
    return create_jwt(
        token_type=TOKEN_TYPE_ACCESS,
        token_data=jwt_payload,
    )


def create_refresh_token(
        schema: UserLoginRequest | UserCreate
) -> str:
    jwt_payload = {
        "sub": schema.email,
    }
    return create_jwt(
        token_type=TOKEN_TYPE_REFRESH,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days)
    )
