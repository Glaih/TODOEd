import logging
from flask import request, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.database import BaseErrors, ValidationErrors, User, Task


logger = logging.getLogger(__name__)


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/api/v1/users/registration/', methods=['POST'])
def create_user():
    auth_request = request.get_json()

    mail, password = get_user_data_from_request(auth_request)

    User.create(email=mail, password=password)
    return {'success': 'User has been registered'}, 200


@api_blueprint.route('/api/v1/users/login', methods=['POST'])
def login_user():
    auth_request = request.get_json()

    mail, password = get_user_data_from_request(auth_request)

    user_id = User.verify(mail, password)

    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    return {'access_token': access_token, 'refresh_token': refresh_token}, 200


@api_blueprint.route('/api/v1/users/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {'access_token': access_token}, 200


@api_blueprint.route('/api/v1/users/jwt_Protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {'user_id': current_user}, 200


@api_blueprint.route('/api/v1/tasks/add', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    task_request = request.get_json()
    title, text, deadline = get_task_data_from_request(task_request['data'])
    task = Task.create(current_user, title, text, deadline)

    return {"data": {"task_id": task.task_id, "title": task.title,
                     "text": task.text, "deadline": task.deadline, "created_at": task.created_at}}, 200


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


def get_task_data_from_request(json_request):
    try:
        title = json_request['title']
        text = json_request['text']

    except TypeError as err:
        logger.exception(f"TYPE_ERROR: {err}")
        raise ValidationErrors({'type_error': f'{err}'})

    except KeyError:
        logger.exception("JSON_KEY_ERROR: 'wrong keys'")
        raise ValidationErrors({'json_key_error': 'wrong keys'})

    deadline = json_request.get('deadline')

    return title, text, deadline
