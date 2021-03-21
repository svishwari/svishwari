"""
Purpose of this file is to house the main application code.
"""
from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

# from huxunify.api.route.home import home_api
# from huxunify.api.route.advertising import advertising_bp
# from huxunify.api.route.decision import decision_bp
# from huxunify.api.route.marketing import marketing_bp
from huxunify.api.route.cdm import (
    datafeeds_search,
    cdm_bp,
    datafeeds_get,
    fieldmappings_search,
    fieldmappings_get,
)


# set config variables
VERSION = "v1"
TITLE = "Hux Unified Solution API"
OPENAPI_VERSION = "2.0"


def create_app():
    """creates the flask app and blueprints

    ---

    Args:

    Returns:
        Response: Returns a flask object

    """
    # setup the flask app
    flask_app = Flask(__name__)

    # setup the configuration
    # flask_app.config.from_object(environ['APP_SETTINGS'])

    # define the api specs
    flask_app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title=TITLE,
                version=VERSION,
                openapi_version=OPENAPI_VERSION,
                plugins=[MarshmallowPlugin()],
            ),
            "APISPEC_SWAGGER_URL": "/swagger/",
            "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",
        }
    )

    # init the flask api spec docs
    docs = FlaskApiSpec(flask_app)

    # register the blueprints
    flask_app.register_blueprint(cdm_bp)

    # register the documents
    docs.register(datafeeds_search, blueprint=cdm_bp.name)
    docs.register(datafeeds_get, blueprint=cdm_bp.name)
    docs.register(fieldmappings_search, blueprint=cdm_bp.name)
    docs.register(fieldmappings_get, blueprint=cdm_bp.name)

    # # register the blueprint and route
    # flask_app.register_blueprint(home_api, url_prefix="/api")
    # flask_app.register_blueprint(advertising_bp, url_prefix="/api/advertising")
    # flask_app.register_blueprint(audience_bp, url_prefix="/api/audience")
    # flask_app.register_blueprint(cdm_bp, url_prefix="/api/cdm")
    # flask_app.register_blueprint(decision_bp, url_prefix="/api/decisioning")
    # flask_app.register_blueprint(marketing_bp, url_prefix="/api/marketing")

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
