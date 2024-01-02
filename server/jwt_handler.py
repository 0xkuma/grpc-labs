import jwt
import logging
import os
from datetime import datetime, timedelta, timezone
from redis_handler import RedisHandler

SECRET_KEY = os.getenv("SECRET_KEY", "secret")


class JWT():
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.redis = RedisHandler()

    def generate_token(self, user_id: str, exp: int) -> str:
        try:
            return jwt.encode({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=exp), "user_id": user_id}, self.secret_key, algorithm="HS256")
        except Exception as e:
            logging.error(e)
            return ""

    def verify_token(self, token: str) -> str:
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except Exception as e:
            logging.error(e)
            return ""

    def decode_token(self, token: str) -> str:
        try:
            return jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])
        except Exception as e:
            logging.error(e)
            raise e

    def verify_token_from_redis(self, token: str) -> str:
        try:
            print("Verifying token from redis")
            user_id = self.decode_token(token)["user_id"]
            token = self.redis.get(f"u:{user_id}:lt")
            if token:
                return jwt.decode(token, self.secret_key, algorithms=["HS256"])
            else:
                return ""
        except Exception as e:
            logging.error(e)
            return ""
