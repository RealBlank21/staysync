from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app import db

ph = PasswordHasher()
PEPPER = "SuperKeySecretVery"

def validate_password(username, password):

    val = db.retrieve_credentials(username)

    if not val:
        return False

    hashed_password = val[2]

    try:
        ph.verify(hashed_password, password + PEPPER)
        return True
    except VerifyMismatchError:
        return False