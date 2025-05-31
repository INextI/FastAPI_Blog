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
    private_key = open("certs/jwt-private.pem", "rb").read()
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=3))
    to_encode.update({"exp": exp})
    encode_jwt = jwt.encode(to_encode, private_key, algorithm="RS256")
    return encode_jwt


def decode_access_token(token: str) -> dict:
    public_key = open("certs/jwt-public.pem", "rb").read()
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Токен истек')
    except jwt.InvalidTokenError:
        raise Exception("Неверный токен")