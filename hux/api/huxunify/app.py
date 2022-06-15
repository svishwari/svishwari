"""Purpose of this file is to house the main application code."""
import logging
from os import environ

import pytz
from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from flask_apscheduler import APScheduler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from huxunify.api.config import get_config
from huxunify.api.prometheus import monitor_app
from huxunify.api.route import ROUTES
from huxunify.api.data_connectors.scheduler import (
    run_scheduled_deliveries,
    run_scheduled_destination_checks,
    run_scheduled_tecton_feature_cache,
    run_scheduled_customer_profile_audience_count,
)
from huxunify.api.route.utils import get_db_client

from huxunify.api import constants as api_c
from huxunify.api.route.utils import get_health_check
from huxunifylib.database.delivery_platform_management import (
    update_pending_delivery_jobs,
)

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

environ[api_c.FLASK_ENV] = get_config().FLASK_ENV


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
    # setup the flask app
    flask_app = Flask(__name__)
    flask_app.testing = flask_app.env == api_c.TEST_MODE

    Limiter(
        flask_app,
        key_func=get_remote_address,
        default_limits=["1000 per minute"],
    )

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

    # only add job if not test mode.
    # TODO: mock scheduled job in flask test client using AsyncIO.
    if (
        flask_app.env != api_c.TEST_MODE
        and not flask_app.config[api_c.DISABLE_SCHEDULED_DELIVERIES]
    ):
        # add delivery schedule cron
        # lowest possible schedule denomination in unified is 15 minutes.
        scheduler.add_job(
            id="process_deliveries",
            func=run_scheduled_deliveries,
            trigger="cron",
            minute=api_c.AUTOMATED_DELIVERY_MINUTE_CRON,
            args=[get_db_client()],
        )
        scheduler.add_job(
            id="process_destination_validations",
            func=run_scheduled_destination_checks,
            trigger="cron",
            minute=api_c.DESTINATION_CHECK_CRON,
            args=[get_db_client()],
        )
        # Schedule caching model features every day at 0000 hours UTC
        scheduler.add_job(
            id="cache_tecton_model_features",
            func=run_scheduled_tecton_feature_cache,
            trigger="cron",
            hour=0,
            timezone=pytz.timezone("US/Eastern"),
            args=[get_db_client()],
        )
        scheduler.add_job(
            id="update_customer_profile_audience_size",
            func=run_scheduled_customer_profile_audience_count,
            trigger="cron",
            hour=1,
            timezone=pytz.timezone("US/Eastern"),
            args=[get_db_client()],
        )
        scheduler.add_job(
            id="process_pending_delivery_jobs",
            func=update_pending_delivery_jobs,
            trigger="cron",
            minute=api_c.DELIVERY_JOB_CRON,
            args=[get_db_client()],
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
    app.run(host="0.0.0.0", port=port, debug=app.debug)  # nosec
