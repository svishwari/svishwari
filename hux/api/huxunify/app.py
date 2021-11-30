"""Purpose of this file is to house the main application code."""
import logging

from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from flask_apscheduler import APScheduler

from huxunify.api.config import load_env_vars
from huxunify.api.prometheus import monitor_app
from huxunify.api.route import ROUTES
from huxunify.api.data_connectors.scheduler import run_scheduled_deliveries

from huxunify.api import constants as api_c
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


def configure_flask(flask_app: Flask) -> None:
    """Set configuration and variables for Flask.

    Args:
        flask_app (Flask): Flask application.

    Raises:
        Exception: Error if the flask app config doesn't have the "ENV" key
            setup appropriately.
    """

    # setup the environment config
    try:
        if flask_app.config["ENV"] == api_c.PRODUCTION_MODE:
            flask_app.config.from_object(
                "huxunify.api.config.ProductionConfig"
            )
        elif flask_app.config["ENV"] == api_c.DEVELOPMENT_MODE:
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
    """creates the flask app and blueprints.

    Returns:
        Flask: Returns a flask object.
    """

    load_env_vars()

    # setup the flask app
    flask_app = Flask(__name__)
    flask_app.testing = flask_app.env == api_c.TEST_MODE

    # setup CORS
    CORS(flask_app)

    # register the routes
    for route in ROUTES:
        logging.debug("Registering %s.", route.name)
        flask_app.register_blueprint(route, url_prefix="/api/v1")

    # add health check URLs
    # pylint: disable=unnecessary-lambda
    flask_app.add_url_rule(
        api_c.HEALTH_CHECK_ENDPOINT,
        api_c.HEALTH_CHECK,
        view_func=lambda: get_health_check().run(),
    )

    # setup the swagger docs
    Swagger(flask_app, config=SWAGGER_CONFIG, merge=True)

    # configure flask
    configure_flask(flask_app)

    # monitor flask setup
    if flask_app.env != api_c.TEST_MODE:
        monitor_app(flask_app)

    # initialize scheduler
    scheduler = APScheduler(app=flask_app)
    scheduler.start()

    # add delivery schedule cron
    # lowest possible schedule denomination in unified is 15 minutes.
    scheduler.add_job(
        id="process_deliveries",
        func=run_scheduled_deliveries,
        trigger="cron",
        minute="15",
    )

    return flask_app


# pylint: disable=no-member
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
    app.run(host="0.0.0.0", port=port, debug=True)  # nosec
