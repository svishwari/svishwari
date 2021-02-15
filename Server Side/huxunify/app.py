"""
Purpose of this file is to house the main application code.
"""
from flask import Flask
from flasgger import Swagger
from api.route.home import home_api
from api.route.advertising import advertising_bp
from api.route.decision import decision_bp
from api.route.cdm import cdm_bp


def create_app():
    """
    create application code,
    store all the routes here.
    :return:
    """
    # setup the flask app
    flask_app = Flask(__name__)

    # setup the api documentation
    flask_app.config['SWAGGER'] = {
        'title': 'HUX Unified Solution API',
    }
    swagger = Swagger(flask_app)

    # register the blueprint and route
    flask_app.register_blueprint(home_api, url_prefix='/api')
    flask_app.register_blueprint(advertising_bp, url_prefix='/api/advertising')
    flask_app.register_blueprint(decision_bp, url_prefix='/api/decision')
    flask_app.register_blueprint(cdm_bp, url_prefix='/api/cdm')

    return flask_app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    # create the API
    app = create_app()

    # run the API
    app.run(host='127.0.0.1', port=port, debug=True)
