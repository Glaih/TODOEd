import re
from flask import jsonify


def validate_mail(email):
    match = re.search(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$", email)
    if match:
        return True
    else:
        return False


def validate_psw(psw):
    if 8 <= len(psw) <= 30:
        return True
    else:
        return False


def validation_response(email, psw):
    if validate_mail(email) and validate_psw(psw):
        return True

    elif not validate_mail(email) and validate_psw(psw):
        return jsonify({'errors': {'email': 'Incorrect email'}}), 400

    elif not validate_psw(psw) and validate_mail(email):
        return jsonify({'errors': {'password': 'Password must be 8 - 30 symbols long'}}), 400

    elif not validate_mail(email) and not validate_psw(psw):
        return jsonify({
                        'errors': {'password': 'Password must be 8 - 30 symbols long',
                                   'email': 'Incorrect email'}}), 400
