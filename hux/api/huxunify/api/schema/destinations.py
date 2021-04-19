# pylint: disable=no-self-use
"""
Schemas for the Destinations API
"""

from flask_marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import OneOf


class DestinationSchema(Schema):
    """
    Destinations schema class
    """

    destinations_id = fields.String(attribute="_id")
    destinations_type = fields.String(attribute="destinations_type")
    destinations_name = fields.String(attribute="name")
    destinations_status = fields.String(
        attribute="connection_status",
        validate=[
            OneOf(choices=["Pending", "In progress", "Failed", "Succeeded"])
        ],
    )
    created = fields.DateTime(attribute="create_time", allow_none=True)
    updated = fields.DateTime(attribute="update_time", allow_none=True)


class FacebookAuthConstants(Schema):
    """
    Facebook Auth constants schema class
    """

    facebook_ad_account_id = fields.String()
    facebook_app_id = fields.String()
    facebook_app_secret = fields.String()
    facebook_access_token = fields.String()


class DestinationConstants(Schema):
    """
    Destination constants schema class
    """

    Facebook = fields.Nested(FacebookAuthConstants)


class SFMCAuthConstants(Schema):
    """
    SFMC Auth constants schema class
    """

    sfmc_account_id = fields.String()
    sfmc_app_id = fields.String()
    sfmc_app_secret = fields.String()
    sfmc_rest_uri = fields.String()
    sfmc_soap_uri = fields.String()
