import jwt
import logging
from datetime import datetime, timedelta, timezone


def generate_token(username: str) -> str:
    try:
        return jwt.encode({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=30), "username": username}, "secret", algorithm="HS256")
    except Exception as e:
        logging.error(e)
        return ""
