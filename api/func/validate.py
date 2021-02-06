import re


def validate_mail(email):
    return re.search(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$", email)


def validate_psw(psw):
    return 8 <= len(psw) <= 30


def validation_response(email, psw):
    if validate_mail(email) and validate_psw(psw):
        return True

    elif not validate_mail(email) and validate_psw(psw):
        return {'errors': {'email': 'Incorrect email'}}, 400
    elif not validate_psw(psw) and validate_mail(email):
        return {'errors': {'password': 'Password must be 8 - 30 symbols long'}}, 400

    elif not validate_mail(email) and not validate_psw(psw):
        return {'errors': {'password': 'Password must be 8 - 30 symbols long',
                           'email': 'Incorrect email'}}, 400
