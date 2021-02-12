from flask import Flask, request
import logging
from pathlib import Path

from func.registration import write_in_usr_db

logging.basicConfig(
    format='%(asctime)s - %(name)s:%(message)s',
    filename=Path(__file__, '../app.log').resolve(),
    level=logging.DEBUG,
)

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route('/api/v1/users/', methods=['POST'])
def registration():
    auth_request = request.get_json()

    try:
        auth_request['email']
        auth_request['password']

    except TypeError as err:
        logger.exception(f"TYPE_ERROR: {err}")
        return {'type_error': f'{err}'}, 400

    except KeyError:
        logger.exception("JSON_KEY_ERROR: 'wrong keys'")
        return {'json_key_error': 'wrong keys'}, 400

    else:
        return write_in_usr_db(auth_request['email'], auth_request['password'])


if __name__ == '__main__':
    app.run(debug=True)
