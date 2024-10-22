from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app import db
import os

try:
    file_path = os.path.join(os.path.dirname(__file__), '../PEPPER.txt')
    with open(file_path, 'r') as file:
        PEPPER = file.read().strip()
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"Error reading file: {e}")

ph = PasswordHasher()

def validate_password(username, password):

    val = db.retrieve_credentials(username)

    if not val:
        return False

    hashed_password = val[3]

    try:
        ph.verify(hashed_password, password + PEPPER)
        return True
    except VerifyMismatchError:
        return False