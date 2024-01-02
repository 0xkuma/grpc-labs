import logging
import string
import re
import random
from psycopg2 import sql
from time import sleep
from tenacity import retry, wait_exponential, stop_after_attempt, RetryError
from argon2 import PasswordHasher, exceptions
from db_handler import Database
from jwt_handler import JWT


class User():
    def __init__(self):
        self.db = Database()
        self.jwt = JWT()
        self.attempts = 0
        self.max_attempts = 1
        self.max_backoff_time = 20

    def get_truncated_exponential_backoff_time(self, attempt: int) -> int:
        """
        The function to calculate the delay for a retry attempt using
        the Truncated Exponential Backoff algorithm.

        Parameters:
        attempt (int): The number of the current retry attempt.

        Returns:
        int: Amount of time to delay.
        """

        delay = min(self.max_backoff_time, 2 * 2 ** attempt)
        jitter = random.uniform(0.5, 1.5)
        print("Delay: ", delay, "Jitter: ", jitter, "Delay * Jitter: ",
              delay * jitter, "Attempt: ", attempt)
        return delay * jitter

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
        while self.attempts < self.max_attempts:
            try:
                print("Creating user")
                res = self.db.execute("INSERT INTO users(username, e_password, salt, email) VALUES (%s, %s, %s, %s) RETURNING user_id", (
                    username, password, salt, email))
                print(res[0])
                if res and res[0]:
                    self.attempts = 0
                    return res[0][0]
                else:
                    self.db.rollback()
                    self.attempts += 1
                    sleep(self.get_truncated_exponential_backoff_time(self.attempts))
                    continue
            except Exception as e:
                logging.error(e)
                self.attempts += 1
                sleep(self.get_truncated_exponential_backoff_time(self.attempts))
                self.db.create_connection()
                continue
        self.attempts = 0
        raise Exception("Failed to create user")

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def update_user(self, token: str, user_info: dict) -> bool:
        global content

        try:
            content = self.jwt.verify_token(token)
            if content == "":
                content = self.jwt.verify_token_from_redis(token)
            if not content:
                raise Exception("Invalid token")
        except Exception as e:
            logging.error(e)
            raise Exception("Failed to update user due to an invalid token.")
        try:
            set_clause = self.db.set_clause(
                user_info.keys(), user_info.values())

            query = sql.SQL(
                "UPDATE user_info SET {} WHERE user_id = (%s) RETURNING user_id")
            command = query.format(set_clause)

            params = (content['user_id'],)

            res = self.db.execute(command, params)

            if not res or not res[0]:
                self.db.rollback()
                raise Exception("Failed to update user. No results returned.")

            return True

        except RetryError as e:
            logging.error(
                "Failed to update user following 3 attempts with error: %s", e)
            raise Exception(
                "Failed to update user following 3 attempts.") from e

        except Exception as e:
            logging.error("Unexpected error during user update: %s", e)
            self.db.create_connection()
            raise Exception(
                "Failed to update user due to an unexpected error.") from e

    def is_user_exists(self, username: str) -> bool:
        try:
            res = self.db.execute(
                "SELECT user_id FROM users WHERE username = %s LIMIT 1", (username,))
            return True if res else False
        except Exception as e:
            logging.error(e)
            return False

    def authenticate_user(self, username: str, password: str) -> bool:
        try:
            res = self.db.execute(
                "SELECT user_id, e_password, salt FROM users WHERE username = %s LIMIT 1", (username,))
            if not res:
                return ""
            user_id, e_password, salt = res[0]
            return user_id if PasswordHasher().verify(e_password, password + salt) else ""
        except exceptions.VerifyMismatchError as e:
            logging.error(e)
            return ""
        except Exception as e:
            logging.error(e)
            return ""
