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
    if validate_mail(email) is True and validate_psw(psw) is True:
        return True

    elif validate_mail(email) is not True and validate_psw(psw) is True:
        return jsonify({'mail_error': 'Invalid Email address'}), 400

    elif validate_psw(psw) is not True and validate_mail(email) is True:
        return jsonify({'psw_error': 'Password must be 8 - 30 symbols long'}), 400

    elif validate_mail(email) is not True and validate_psw(psw) is not True:
        return jsonify({
                        'mail_error': 'Invalid Email address',
                        'psw_error': 'Password must be 8 - 30 symbols long'
                       }), 400