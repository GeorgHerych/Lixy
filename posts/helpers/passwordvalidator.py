import re

def is_password_valid(password):
    is_valid = True
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[_])[A-Za-z\d_]{8,}$"

    if len(password) < 8:
        is_valid = False

    if password.isdigit():
        is_valid = False

    if is_valid:
        is_valid = re.search(regex, password)

    return is_valid