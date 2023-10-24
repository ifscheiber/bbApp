import bcrypt
import secrets
import string
import smtplib

import json
from flask import current_app, request
from itsdangerous import URLSafeTimedSerializer

from emails.automatic_emails import WelcomeNewUserEmail, ResetPasswordLinkEmail

from datetime import datetime

from data.models.user_orm import LeapNodeBillingUser
from data.data_handler import ScopedSession


def check_hash(email: str, password: str):
    """
    Verify the hashed password for a given email.

    This function takes an email and a password as input and checks the hashed password
    stored in the database for the given email. It uses bcrypt to compare the hashed
    password with the given password.

    :param email: The email of the user whose password needs to be verified.
    :type email: str
    :param password: The password to be verified.
    :type password: str
    :return: A tuple where the first element is a boolean indicating the result of the
             password check (True if the password is correct, False otherwise), and the
             second element is the user object retrieved from the database.
    :rtype: tuple[bool, LeapNodeBillingUser]
    """
    session = ScopedSession()

    user: LeapNodeBillingUser = session.query(LeapNodeBillingUser).filter(LeapNodeBillingUser.email == email).first()

    hash_result = False

    if user:
        byte_block = password.encode()
        hashed = user.password.encode()
        hash_result = bcrypt.checkpw(byte_block, hashed)

    return hash_result, user


def create_user(user_id, user_email, user_role, path_to_credentials: str):

    valid_credentials = json.load(open(path_to_credentials))

    if user_id in valid_credentials:
        print('User-ID already in use')  # TODO: INFORM MESSAGE IN FRONTEND, stay on modal and mark red user_id
        return

    hashed_password, initial_password = generate_password()
    new_user = dict(password=hashed_password.decode(), email=user_email, role=user_role)

    # ------------------------------------------------------------------------------------------------------------------
    # send Welcome Email
    # ------------------------------------------------------------------------------------------------------------------
    e = WelcomeNewUserEmail(
        sender='leapnode@gmail.com',
        recipient=user_email,
        user_id=user_id,
        initial_password=initial_password,
        smtp_server=smtplib.SMTP('localhost', port=1025)
    )
    e.send_email()

    valid_credentials.update({user_id: new_user})
    with open(path_to_credentials, 'w') as f:
        f.write(json.dumps(valid_credentials, indent=4))

    #  TODO send automatic email
    # TODO INFORM MESSAGE IN FRONTEND


def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    hashed_password = hash_salt(password)
    return hashed_password, password


def update_password(new_password, user_id, path_to_credentials: str):
    valid_credentials = json.load(open(path_to_credentials))
    valid_credentials[user_id]['password'] = hash_salt(new_password.encode()).decode()
    with open(path_to_credentials, 'w') as f:
        f.write(json.dumps(valid_credentials, indent=4))


def hash_salt(password):
    """
    Hash and salt a given password.

    This function takes a password as input, generates a new random salt, and returns the hashed
    version of the password combined with the salt. It uses bcrypt for hashing and salting.

    :param password: The password to be hashed and salted.
    :type password: str
    :return: The hashed and salted password.
    :rtype: bytes
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    return hashed


# ------------------------------------------------------------------------------------------------------------------
# Confirmation-Token, Password-Reset-Token
# ------------------------------------------------------------------------------------------------------------------
def send_reset_password_link(user_email, user_id, endpoint, salt):
    token_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = token_serializer.dumps(user_id, salt=salt)
    url = f'http://{request.base_url.split("//")[-1].split("/")[0]}/reset-password/{token}'
    # ------------------------------------------------------------------------------------------------------------------
    # Send Welcome Email
    # ------------------------------------------------------------------------------------------------------------------
    e = ResetPasswordLinkEmail(
        sender='mitoann@gmail.com',
        recipient=user_email,
        user_id=user_id,
        url=url,
        smtp_server=smtplib.SMTP('localhost', port=1025)
    )
    e.send_email()



if __name__ == '__main__':
    print(f"CHECK: {check_hash('ifscheiber@gmail.com', 'Leah2017!')}")

    user_ids = [1, 2, 3]
    first_names = ['Lennart', 'Ivo', 'Jannis']
    middle_name = ['Jan', 'Florin', None]
    last_names = ['Scheiber']*3
    user_emails = ['lennart.scheiber@gmail.com', 'ifscheiber@gmail.com', 'jannisscheiber@gmail.com']
    passwords = ['lennart', 'Leah2017!', 'jannis']
    status = [1]*3
    registration_dates = [datetime.today()]*3
    roles = ['admin'] * 2 + ['analyst']
    clients = ['LeapNode'] * 3

    user_attr = zip(user_ids, first_names, middle_name, last_names, user_emails, passwords, status, registration_dates,
                    roles, clients)

    session = ScopedSession()

    for i, fn, mn, ln, e, p, s, rd, r, c in user_attr:
        hp = hash_salt(p).decode()
        new_user = LeapNodeBillingUser(
            id=i, first_name=fn, middle_names=mn, last_name=ln, email=e, password=hp, status=s, registration_date=rd,
            role=r, client=c
        )
        session.add(new_user)

    session.commit()










