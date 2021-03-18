"""
Purpose of this file is to house the main application code.
"""
from flask import Flask, redirect
from flasgger import Swagger
from huxunify.api.route.home import home_api
from huxunify.api.route.advertising import advertising_bp
from huxunify.api.route.decision import decision_bp
from huxunify.api.route.marketing import marketing_bp
from huxunify.api.route.cdm import cdm_bp
from huxunify.api.route.audience import audience_bp


def create_app():
    """
    create application code,
    store all the routes here.
    :return:
    """
    # setup the flask app
    flask_app = Flask(__name__)

    # setup the configuration
    # flask_app.config.from_object(environ['APP_SETTINGS'])

    # setup the api documentation
    flask_app.config["SWAGGER"] = {
        "title": "Hux Unified Solution API",
    }
    Swagger(flask_app)

    # default just send user over to apidocs
    @flask_app.route("/")
    def index():
        return redirect("/apidocs")

    # register the blueprint and route
    flask_app.register_blueprint(home_api, url_prefix="/api")
    flask_app.register_blueprint(advertising_bp, url_prefix="/api/advertising")
    flask_app.register_blueprint(audience_bp, url_prefix="/api/audience")
    flask_app.register_blueprint(cdm_bp, url_prefix="/api/cdm")
    flask_app.register_blueprint(decision_bp, url_prefix="/api/decisioning")
    flask_app.register_blueprint(marketing_bp, url_prefix="/api/marketing")

    return flask_app


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    args = parser.parse_args()
    port = args.port

    # create the API
    app = create_app()

    # run the API
    app.run(host="127.0.0.1", port=port, debug=True)
