from datetime import datetime, timedelta, timezone
from typing import Any, Union

import jwt
from app.core.security_config import pwd_context

from app.core.config import settings
from app.core.security import pwd_context



ALGORITHM = "HS256"


def create_access_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)