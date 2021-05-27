"""
Purpose of this file is to house the main application code.
"""
from requests import Response
from flask import Flask
from flasgger import Swagger
from flask_cors import CORS

from huxunify.api.config import load_env_vars
from huxunify.api.route import ROUTES
from huxunify.api import constants
from huxunify.api.route.utils import get_health_check


# set config variables
SWAGGER_CONFIG = {
    "uiversion": "3",
    "static_url_path": "/swagger",
    "title": "Hux API",
    "version": "1.0.0",
    "swagger_ui": True,
    "specs_route": "/api/v1/ui/",
    "description": "",
    "termsOfService": "",
    "schemes": ["https"],
    "securityDefinitions": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}


def after_request(response) -> Response:
    """Set configuration and variables for Flask.

    Args:
        response (Response): App after request response.

    Returns:
        Response: returns the response with added headers.

    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "PUT,GET,POST,DELETE"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type,Authorization"
    return response


def configure_flask(flask_app: Flask) -> None:
    """Set configuration and variables for Flask.

    Args:
        flask_app (Flask): Flask application.

    Returns:

    """
    # setup the environment config
    try:
        if flask_app.config["ENV"] == constants.PRODUCTION_MODE:
            flask_app.config.from_object(
                "huxunify.api.config.ProductionConfig"
            )
        elif flask_app.config["ENV"] == constants.DEVELOPMENT_MODE:
            flask_app.config.from_object(
                "huxunify.api.config.DevelopmentConfig"
            )
        else:
            # use http by default for local testing.
            SWAGGER_CONFIG["schemes"].insert(0, "http")
            flask_app.config.from_object("huxunify.api.config.Config")
    except KeyError as error:
        desc = f"Environment not configured: {error} is required."
        raise Exception(desc) from error


def create_app() -> Flask:
    """creates the flask app and blueprints

    Args:

    Returns:
        Flask: Returns a flask object.

    """
    load_env_vars()

    # setup the flask app
    flask_app = Flask(__name__)

    CORS(flask_app)

    # assign the after request call
    flask_app.after_request(after_request)

    # register the routes
    for route in ROUTES:
        print(f"Registering {route.name}.")
        flask_app.register_blueprint(route, url_prefix="/api/v1")

    # add health check URLs
    # pylint: disable=unnecessary-lambda
    flask_app.add_url_rule(
        constants.HEALTH_CHECK_ENDPOINT,
        constants.HEALTH_CHECK,
        view_func=lambda: get_health_check().run(),
    )

    # setup the swagger docs
    Swagger(flask_app, config=SWAGGER_CONFIG, merge=True)

    # configure flask
    configure_flask(flask_app)

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
    app.run(host="0.0.0.0", port=port, debug=True)
