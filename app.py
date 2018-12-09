import os
from flask import jsonify, make_response, send_from_directory

from app import app


PORT = 5000


@app.errorhandler(404)
def not_found(error):
    """ error handler """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # LOG.info('running environment: %s', os.environ.get('ENV'))
    # app.config['DEBUG'] = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT))
