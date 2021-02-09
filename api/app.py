from flask import Flask, request
import logging
from pathlib import Path

from func.registration import write_in_usr_db

logging.basicConfig(
    format='%(asctime)s - %(name)s:%(message)s',
    filename=Path(__file__, '../app.log').resolve(),
    level=logging.info,
)

app = Flask(__name__)

logger = logging.getLogger(__name__)


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


