"""
Purpose of this file is to house the main application code.
"""
import yaml
from flask import Flask, jsonify
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint
from huxunify.api.route.home import home_api
from huxunify.api.route.advertising import advertising_bp
from huxunify.api.route.decision import decision_bp
from huxunify.api.route.audience import audience_bp
from huxunify.api.route.marketing import marketing_bp
from huxunify.api.route.cdm import cdm_bp
from huxunify.api.schema.cdm import Datafeed, Fieldmapping


# set config variables
SWAGGER_URL = "/api/docs"
API_URL = "/api/swagger.json"
TITLE = "Hux Unified Solution API"
VERSION = "0.0.1"
OPENAPI_VERSION = "3.0.2"

# define openapi spec to later load into YAML
# here we can define servers, and all other common api spec items.
OPENAPI_SPEC = f"""
openapi: {OPENAPI_VERSION}
info:
  description: Hux Unified Solution API document
  title: {TITLE}
  version: {VERSION}
"""


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

    # init the flask api spec docs
    spec = APISpec(
        title=TITLE,
        version=VERSION,
        openapi_version=OPENAPI_VERSION,
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        **yaml.safe_load(OPENAPI_SPEC),
    )

    # Call factory function to create our blueprint
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "HUX Unified Solution"}
    )

    # register the blueprints
    flask_app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    flask_app.register_blueprint(cdm_bp, url_prefix="/cdm")

    # register marshmallow specs
    spec.components.schema("Datafeed", schema=Datafeed)
    spec.components.schema("Fieldmapping", schema=Fieldmapping)

    # register all the swagger docs here in each blueprint
    with flask_app.test_request_context():
        # register all swagger documented functions here
        for fn_name in flask_app.view_functions:
            if fn_name == "static":
                continue
            print(f"Loading swagger docs for function: {fn_name}")
            view_fn = flask_app.view_functions[fn_name]
            spec.path(view=view_fn)

    # register the blueprint and route
    flask_app.register_blueprint(home_api, url_prefix="/api")
    flask_app.register_blueprint(advertising_bp, url_prefix="/api/advertising")
    flask_app.register_blueprint(audience_bp, url_prefix="/api/audience")
    flask_app.register_blueprint(decision_bp, url_prefix="/api/decisioning")
    flask_app.register_blueprint(marketing_bp, url_prefix="/api/marketing")

    # define the swagger route for generating the swagger json
    @flask_app.route("/api/swagger.json")
    def create_swagger_spec():  # pylint: disable=unused-variable
        return jsonify(spec.to_dict())

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
