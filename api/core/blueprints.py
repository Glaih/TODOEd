import logging
from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity

from core.database import BaseErrors, ValidationErrors, User


logger = logging.getLogger(__name__)


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/api/v1/users/registration/', methods=['POST'])
def registration():
    auth_request = request.get_json()

    mail, password = get_user_data_from_request(auth_request)

    User.create(email=mail, password=password)
    return {'success': 'User has been registered'}, 200


@api_blueprint.route('/api/v1/users/login', methods=['POST'])
def login():
    auth_request = request.get_json()

    mail, password = get_user_data_from_request(auth_request)

    User.verify_user(mail, password)

    access_token = create_access_token(identity=mail)
    refresh_token = create_refresh_token(identity=mail)
    return {'access_token': access_token, 'refresh_token': refresh_token}, 200


@api_blueprint.route('/api/v1/users/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {'access_token': access_token}, 200


@api_blueprint.route('/api/v1/users/jwt_Protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {'logged_in_as': current_user}, 200


@api_blueprint.errorhandler(BaseErrors)
def handle_bad_verification(e):
    logger.exception(e)
    return e.get_errors(), e.status_code


def get_user_data_from_request(json_request):
    try:
        mail = json_request['email']
        password = json_request['password']
        return mail, password

    except TypeError as err:
        logger.exception(f"TYPE_ERROR: {err}")
        raise ValidationErrors({'type_error': f'{err}'})

    except KeyError:
        logger.exception("JSON_KEY_ERROR: 'wrong keys'")
        raise ValidationErrors({'json_key_error': 'wrong keys'})
