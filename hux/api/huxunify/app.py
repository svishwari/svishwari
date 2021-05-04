"""
Purpose of this file is to house the main application code.
"""
from flask import Flask
from flasgger import Swagger
from huxunify.api.route.destination import dest_bp
from huxunify.api.route.cdm import cdm_bp
from huxunify.api.route.user import user_bp
from huxunify.api.route.authenticate import auth_bp
from huxunify.api.route.audience import audience_bp


# set config variables
SWAGGER_URL = "/api/docs"
API_URL = "/api/swagger.json"
TITLE = "Hux API"
VERSION = "0.0.1"
OPENAPI_VERSION = "3.0.2"

# define openapi spec to later load into YAML
# here we can define servers, and all other common api spec items.
OPENAPI_SPEC = f"""
openapi: {OPENAPI_VERSION}
info:
  description: Hux API Documentation
  title: {TITLE}
  version: {VERSION}
"""


def create_app():
    """creates the flask app and blueprints

    Args:

    Returns:
        Response: Returns a flask object

    """
    # setup the flask app
    flask_app = Flask(__name__)

    # setup the configuration
    # flask_app.config.from_object(environ['APP_SETTINGS'])

    # register the blueprints
    flask_app.register_blueprint(cdm_bp, url_prefix="/cdm")
    flask_app.register_blueprint(dest_bp, url_prefix="/")
    flask_app.register_blueprint(user_bp, url_prefix="/")
    flask_app.register_blueprint(auth_bp, url_prefix="/")
    flask_app.register_blueprint(audience_bp, url_prefix="/")
    Swagger(flask_app)

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
