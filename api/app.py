from flask import Flask, request
from func.registration import write_in_usr_db
from app_logger import app_logger


app = Flask(__name__)

logger = app_logger(__name__)


@app.route('/api/v1/users/', methods=['POST'])
def registration():
    try:
        auth_request = request.get_json()
        logger.info('JSON acquired')
        return write_in_usr_db(auth_request['email'], auth_request['password'])

    except TypeError:
        logger.exception("TYPE_ERROR: 'data must be in json format'")
        return {'type_error': 'data must be in json format'}, 400
    except KeyError:
        logger.exception("JSON_KEY_ERROR: 'wrong keys'")
        return {'json_key_error': 'wrong keys'}, 400


if __name__ == '__main__':
    app.run(debug=True)


