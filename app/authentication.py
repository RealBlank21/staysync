from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app import db
import os
import re

try:
    file_path = os.path.join(os.path.dirname(__file__), '../PEPPER.txt')
    with open(file_path, 'r') as file:
        PEPPER = file.read().strip()
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"Error reading file: {e}")

ph = PasswordHasher()

def validate_password(ic, password):

    val = db.retrieve_credentials(ic)

    if not val:
        return False

    hashed_password = val['password']

    try:
        ph.verify(hashed_password, password + PEPPER)
        return True
    except VerifyMismatchError:
        return False
    
def validate_form_data(form_data):
    ic = form_data.get('student_ic', '').strip()

    existing_ic = db.ic_check(ic)

    if existing_ic:
        return "Record already existed."

    if len(ic) != 12 or not ic.isdigit():
        return "Invalid IC. It must be 12 digits long and contain only numbers."

    email = form_data.get('student_email', '').strip()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format."

    form_class = form_data.get('form_class', '').strip()
    if not re.match(r"^[1-6][A-E]$", form_class):
        return "Invalid class format. It should be a number (1-6) followed by a letter (A-E)."

    try:
        family_members = int(form_data.get('family_members', '').strip())
        home_distance = int(form_data.get('home_distance', '').strip())
    except ValueError:
        return "Family members and home distance must be valid integers."

    guardian_contact = form_data.get('guardian_contact', '').strip()
    if not re.match(r"^01[0-9]{8,9}$", guardian_contact):
        return "Invalid guardian contact. It must be a valid Malaysian phone number starting with 01."

    return None