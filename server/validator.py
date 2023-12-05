import string


def is_validate_password(password: str) -> bool:
    if len(password) <= 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in string.punctuation:
            has_special = True

        if has_upper and has_lower and has_digit and has_special:
            return True

    return False
