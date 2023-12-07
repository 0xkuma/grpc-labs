import logging
import string
import re
import random
from time import sleep
from db_handler import Database
from argon2 import PasswordHasher, exceptions


class User():
    def __init__(self):
        self.db = Database()
        self.attempts = 0
        self.max_attempts = 3
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
