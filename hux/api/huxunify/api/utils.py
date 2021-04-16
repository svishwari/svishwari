"""
purpose of this file is to house route utilities
"""

from bson import ObjectId

# TODO: Fetch connectors from connector lib

from huxunifylib.database import (
    delivery_platform_management as destination_management,
    constants as db_constants,
)


def add_view_to_blueprint(self, rule, endpoint, **options):
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

    def decorator(cls):
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


# pylint: disable=W0613
def get_connector(platform_type, auth_details_secrets) -> object:
    """Returns a destinations connector.

    Args:
        platform_type (str): Platform type.
        auth_details_secrets (dict): Authentication details.

    Returns:
        destinations connector.
    """
    connector = None
    # TODO : Update to use connectors from connector lib
    if platform_type == db_constants.DELIVERY_PLATFORM_FACEBOOK:
        connector = None
        # connector = FacebookConnector(auth_details=auth_details_secrets)
    elif platform_type == db_constants.DELIVERY_PLATFORM_SFMC:
        connector = None
        # connector = SFMCConnector(auth_details=auth_details_secrets,)
    return connector


def test_destinations_connection(
    destination_id: str, platform_type: str, auth_details: dict
):
    """Test the connection to the destinations and update the
    connection status.
    Args:
        destination_id (str): The destinations ID.
    Returns:
        updated_platform (dict): The updated destinations.
    """

    dp_connector = get_connector(
        platform_type=platform_type,
        auth_details_secrets=auth_details,
    )
    status = dp_connector.check_connection()

    if status:
        connection_status = db_constants.STATUS_SUCCEEDED
    else:
        connection_status = db_constants.STATUS_FAILED

    updated_platform = destination_management.set_connection_status(
        database=None,  # TODO : use mongo connector library to get mongo db client
        delivery_platform_id=ObjectId(destination_id),
        connection_status=connection_status,
    )
    return updated_platform
