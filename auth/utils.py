import jwt

from core.config import settings
from datetime import datetime, timedelta, timezone


def encode_jwt(payload: dict,
               private_key: str = settings.auth_jwt.private_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm
               ):
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
               token: str | bytes,
               public_key: str = settings.auth_jwt.public_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm,
               ):
    decode = jwt.decode(token, public_key, algorithms=[algorithm])
    return decode


def create_access_token(data: dict, expires_delta: timedelta | None = None) ->str:
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=3))
    to_encode.update({"exp": exp})
    return encode_jwt(to_encode)


def decode_access_token(token: str) -> dict:
    try:
        return decode_jwt(token)
    except jwt.ExpiredSignatureError:
        raise Exception('Refresh token expired')
    except jwt.InvalidTokenError:
        raise Exception("Invalid access token")
    

def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days = 7))
    to_encode.update({"exp" : expire})
    return encode_jwt(to_encode)

def decode_refresh_token(token: str) -> dict:
    try:
        return decode_jwt(token)
    except jwt.ExpiredSignatureError:
        raise Exception("Refresh token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid refersh token")