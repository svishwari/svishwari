# pylint: disable=no-self-use
"""
Schemas for the Destinations API
"""

from flask_marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import OneOf
from huxunify.api import constants as api_c
from huxunifylib.database import constants as db_c


class DestinationGetSchema(Schema):
    """
    Destinations schema class
    """

    destinations_id = fields.String(
        attribute=api_c.DESTINATION_ID, example="5f5f7262997acad4bac4373b"
    )
    destinations_type = fields.String(
        attribute=api_c.DESTINATION_TYPE, example="Facebook"
    )
    destinations_name = fields.String(
        attribute=api_c.DESTINATION_NAME, example="My destination"
    )
    destinations_status = fields.String(
        attribute=api_c.DESTINATION_STATUS,
        validate=[
            OneOf(
                choices=[
                    db_c.STATUS_PENDING,
                    db_c.STATUS_IN_PROGRESS,
                    db_c.STATUS_FAILED,
                    db_c.STATUS_SUCCEEDED,
                ]
            )
        ],
    )
    campaigns = fields.Int(
        attribute=api_c.DESTINATION_CAMPAIGN_COUNT, example=5, read_only=True
    )
    campaigns = fields.Int(
        attribute=api_c.DESTINATION_CAMPAIGN_COUNT, example=5, read_only=True
    )
    created = fields.DateTime(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = fields.DateTime(attribute=db_c.CREATED_BY, allow_none=True)
    updated = fields.DateTime(attribute=db_c.UPDATED_BY, allow_none=True)
    updated_by = fields.DateTime(attribute=db_c.UPDATE_TIME, allow_none=True)


class DestinationPutSchema(Schema):
    """
    Destination put schema class
    """

    destination_type = fields.String()
    destination_name = fields.String()
    authentication_details = fields.Field()


class DestinationPostSchema(DestinationPutSchema):
    """
    Destination post schema class
    """

    destination_type = fields.String(required=True)
    destination_name = fields.String(required=True)
    authentication_details = fields.Field(required=True)


class FacebookAuthConstants(Schema):
    """
    Facebook Auth constants schema class
    """

    facebook_ad_account_id = fields.String()
    facebook_app_id = fields.String()
    facebook_app_secret = fields.String()
    facebook_access_token = fields.String()


class SFMCAuthConstants(Schema):
    """
    SFMC Auth constants schema class
    """

    sfmc_account_id = fields.String()
    sfmc_app_id = fields.String()
    sfmc_app_secret = fields.String()
    sfmc_rest_uri = fields.String()
    sfmc_soap_uri = fields.String()


class DestinationConstants(Schema):
    """
    Destination constants schema class
    """

    Facebook = fields.Nested(FacebookAuthConstants)
    SFMC = fields.Nested(SFMCAuthConstants)
