"""
purpose of this file is to house route utilities
"""
from typing import Any
from pymongo import MongoClient
from huxunify.api.config import MONGO_DB_CONFIG
from huxunifylib.connectors.util.client import db_client_factory


def add_view_to_blueprint(self, rule: str, endpoint: str, **options) -> Any:
    """
    This decorator takes a blueprint and assigns the view function directly
    the alternative to this is having to manually define this in app.py
    or at the bottom of the route file, as the input is a class.

    app.add_url_rule(
        '/colors/<palette>',
        view_func=PaletteView.as_view('colors'),
        methods=['GET']
    )

    Example: @add_view_to_blueprint(cdm_bp, "/datafeeds", "DatafeedSearch")

    Args:
        self (func): a flask/blueprint object, must have 'add_url_rule'
        rule (str): an input rule
        endpoint (str): the name of the endpoint

    Returns:
        Response: decorator

    """

    def decorator(cls) -> Any:
        """decorator function

        Args:
            cls (object): a function to decorate

        Returns:
            Response: Returns the decorated object.

        """
        # add the url to the flask object
        self.add_url_rule(rule, view_func=cls.as_view(endpoint), **options)
        return cls

    return decorator


def get_db_client() -> MongoClient:
    """Get DB client.
    Returns:
        MongoClient: MongoDB client.
    """
    return db_client_factory.get_resource(**MONGO_DB_CONFIG)
