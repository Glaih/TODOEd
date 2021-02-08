from flask import Flask, request
from func.registration import write_in_usr_db
import logging


app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s:%(message)s',
                    filename='app.log',
                    level=logging.INFO)


@app.route('/api/v1/users/', methods=['POST'])
def registration():
    try:
        auth_request = request.get_json()
        logger.info('JSON acquired')
        return write_in_usr_db(auth_request['email'], auth_request['password'])

    except TypeError:
        logger.exception('type_error: data must be in json format')
        return {'type_error': 'data must be in json format'}, 400
    except KeyError:
        logger.exception('json_key_error: wrong keys')
        return {'json_key_error': 'wrong keys'}, 400


if __name__ == '__main__':
    logger.debug('app starts')
    app.run(debug=True)


