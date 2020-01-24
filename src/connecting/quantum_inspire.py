from getpass import getpass
from quantuminspire.credentials import get_token_authentication, get_basic_authentication


def get_authentication(qi_email=None, qi_password=None, token=None):
    """ Gets the authentication for connecting to the Quantum Inspire API."""
    if token is not None:
        return get_token_authentication(token)
    else:
        if qi_email is None or qi_password is None:
            print('Enter email')
            email = input()
            print('Enter password')
            password = getpass()
        else:
            email, password = qi_email, qi_password
        return get_basic_authentication(email, password)