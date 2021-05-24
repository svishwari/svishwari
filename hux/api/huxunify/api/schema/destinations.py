# pylint: disable=no-self-use
"""
Schemas for the Destinations API
"""

from flask_marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import OneOf
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import (
    must_not_be_blank,
    validate_object_id,
)


class DestinationGetSchema(Schema):
    """
    Destinations schema class
    """

    _id = fields.String(
        data_key=api_c.ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    type = fields.String(
        attribute=api_c.DELIVERY_PLATFORM_TYPE, example="Facebook"
    )
    name = fields.String(
        attribute=api_c.DESTINATION_NAME, example="My destination"
    )
    status = fields.String(
        attribute=api_c.CONNECTION_STATUS,
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
    create_time = fields.String(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = fields.String(attribute=db_c.CREATED_BY, allow_none=True)
    update_time = fields.String(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = fields.String(attribute=db_c.UPDATED_BY, allow_none=True)


class DestinationPutSchema(Schema):
    """
    Destination put schema class
    """

    authentication_details = fields.Field()


class DestinationValidationSchema(Schema):
    """
    Destination put schema class
    """

    authentication_details = fields.Field()
    type = fields.String()


class FacebookAuthConstants(Schema):
    """
    Facebook Auth constants schema class
    """

    facebook_ad_account_id = fields.String(
        required=True, validate=must_not_be_blank
    )
    facebook_app_id = fields.String(required=True, validate=must_not_be_blank)
    facebook_app_secret = fields.String(
        required=True, validate=must_not_be_blank
    )
    facebook_access_token = fields.String(
        required=True, validate=must_not_be_blank
    )


class SFMCAuthConstants(Schema):
    """
    SFMC Auth constants schema class
    """

    sfmc_client_id = fields.String(required=True, validate=must_not_be_blank)
    sfmc_account_id = fields.String(required=True, validate=must_not_be_blank)
    sfmc_client_secret = fields.String(
        required=True, validate=must_not_be_blank
    )
    sfmc_auth_base_uri = fields.String(
        required=True, validate=must_not_be_blank
    )
    sfmc_rest_base_uri = fields.String(
        required=True, validate=must_not_be_blank
    )
    sfmc_soap_base_uri = fields.String(
        required=True, validate=must_not_be_blank
    )


class DestinationConstants(Schema):
    """
    Destination constants schema class
    """

    Facebook = fields.Nested(FacebookAuthConstants)
    SFMC = fields.Nested(SFMCAuthConstants)
