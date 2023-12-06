import logging
import string
import re
from db_handler import Database
from argon2 import PasswordHasher, exceptions


class User():
    def __init__(self):
        self.db = Database()

    @staticmethod
    def is_validate_password(password: str) -> bool:
        if len(password) <= 8:
            return False

        has_upper = re.search('[A-Z]', password) is not None
        has_lower = re.search('[a-z]', password) is not None
        has_digit = re.search('[0-9]', password) is not None
        has_special = re.search(
            '[' + string.punctuation + ']', password) is not None

        if has_upper and has_lower and has_digit and has_special:
            return True

        return False

    def create_user(self, username: str, password: str, salt: str, email: str) -> str:
        try:
            res = self.db.execute("INSERT INTO users(username, e_password, salt, email) VALUES (%s, %s, %s, %s) RETURNING user_id", (
                username, password, salt, email))
            return res[0][0]
        except Exception as e:
            logging.error(e)
            return ""

    def is_user_exists(self, username: str) -> bool:
        try:
            res = self.db.execute(
                "SELECT user_id FROM users WHERE username = %s", (username,))
            return True if res else False
        except Exception as e:
            logging.error(e)
            return False

    def authenticate_user(self, username: str, password: str) -> bool:
        try:
            res = self.db.execute(
                "SELECT e_password, salt FROM users WHERE username = %s", (username,))
            if not res:
                return False
            e_password, salt = res[0]
            return PasswordHasher().verify(e_password, password + salt)
        except exceptions.VerifyMismatchError as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(e)
            return False
