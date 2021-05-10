"""
Purpose of this file is to house the main application code.
"""
from flask import Flask
from flasgger import Swagger
from flask_cors import CORS

from huxunify.api.route import ROUTES


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
}


def create_app() -> Flask:
    """creates the flask app and blueprints

    Args:

    Returns:
        Flask: Returns a flask object.

    """
    # setup the flask app
    flask_app = Flask(__name__)
    CORS(flask_app)

    # register the routes
    for route in ROUTES:
        print(f"Registering {route.name}.")
        flask_app.register_blueprint(route, url_prefix="/api/v1")

    # setup the swagger docs
    Swagger(flask_app, config=SWAGGER_CONFIG, merge=True)

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
