import re


def isValidEmail(email):
    """
    Verifies that an email is in proper format
    :param email
    """
    return re.match(r'[^@]+@[^@]+\.[^@]+', email)