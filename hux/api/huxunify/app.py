"""
Purpose of this file is to house the main application code.
"""
from typing import Union, List
from flask import Flask
from flasgger import Swagger
from werkzeug import Response
from werkzeug.wsgi import ClosingIterator
from flask_cors import CORS

from huxunify.api.route import ROUTES


# set config variables
SWAGGER_CONFIG = {
    "openapi": "3.0.3",
    "uiversion": "3",
    "static_url_path": "/swagger",
    "title": "HUX API",
    "version": "1.0.0",
    "swagger_ui": True,
    "specs_route": "/ui/",
    "description": "",
    "termsOfService": "",
    "servers": [
        {"url": "http://localhost:5000/api/v1", "description": ""},
    ],
    "components": [],
    "securityDefinitions": {
        "oAuthSample": {
            "type": "oauth2",
            "flow": "application",
            "tokenUrl": "",
        }
    },
}


class PrefixMiddleware:
    """PrefixMiddleware class"""

    def __init__(self, wsgi_app: Flask.wsgi_app, prefix: str = ""):
        """Creates middleware for serving flask under a url prefix.

        Args:
              wsgi_app (Flask.wsgi_app): flask wsgi_app.
              prefix (str): Url prefix.

        Returns:

        """
        self.app = wsgi_app
        self.prefix = prefix

    def __call__(
        self, environ: dict, response: Response
    ) -> Union[ClosingIterator, List[str]]:
        """Method when the class is called that binds the url prefix.

        Args:
              environ (dict): flask env dict.
              response (Response): flask wsgi response.

        Returns:
             ClosingIterator: return wsgi closing iterator.
        """
        if environ["PATH_INFO"].startswith(self.prefix):
            environ["PATH_INFO"] = environ["PATH_INFO"][len(self.prefix) :]
            environ["SCRIPT_NAME"] = self.prefix
            return self.app(environ, response)

        response("404", [("Content-Type", "text/plain")])
        return ["This url does not belong to the app.".encode()]


def create_app() -> Flask:
    """creates the flask app and blueprints

    Args:

    Returns:
        Flask: Returns a flask object.

    """
    # setup the flask app
    flask_app = Flask(__name__)
    CORS(flask_app, resources={r"/api/*": {"origins": "*"}})

    # register the routes
    for route in ROUTES:
        print(f"Registering {route.name}.")
        flask_app.register_blueprint(route)

    # setup the swagger docs
    Swagger(flask_app, config=SWAGGER_CONFIG, merge=True)

    # set middleware so we can assign the prefixed url.
    flask_app.wsgi_app = PrefixMiddleware(flask_app.wsgi_app, prefix="/api/v1")

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
