import connexion
from connexion.resolver import RestyResolver


def create_app():
    """Sets up a Connexion app using the OpenAPI specification.

    Returns:
      app (FlaskApp): The Flask application backend.
    """
    cxn = connexion.FlaskApp(__name__)
    cxn.add_api("cdm/spec.yaml", resolver=RestyResolver("endpoints"))
    return cxn.app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
