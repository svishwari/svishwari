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
        attribute=api_c.DELIVERY_PLATFORM_TYPE, example="facebook"
    )
    name = fields.String(attribute=api_c.DESTINATION_NAME, example="Facebook")
    status = fields.String(
        attribute=api_c.CONNECTION_STATUS,
        validate=[
            OneOf(
                choices=[
                    api_c.STATUS_NOT_DELIVERED,
                    api_c.STATUS_DELIVERING,
                    api_c.STATUS_DELIVERED,
                    api_c.STATUS_DELIVERY_PAUSED,
                    api_c.STATUS_ERROR,
                ]
            )
        ],
    )
    campaigns = fields.Int(
        attribute=api_c.DESTINATION_CAMPAIGN_COUNT, example=5, read_only=True
    )
    performance_de = fields.Dict(
        attribute=db_c.PERFORMANCE_METRICS_DATA_EXTENSION,
        example={
            api_c.NAME: db_c.DELIVERY_PLATFORM_SFMC,
            api_c.DATA_EXTENSION_ID: "5f5f7262997acad4bac4373c",
        },
        required=False,
        allow_none=True,
    )
    is_added = fields.Bool(attribute="added")
    is_enabled = fields.Bool(attribute="enabled")
    create_time = fields.String(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = fields.String(attribute=db_c.CREATED_BY, allow_none=True)
    update_time = fields.String(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = fields.String(attribute=db_c.UPDATED_BY, allow_none=True)


class DestinationPutSchema(Schema):
    """
    Destination put schema class
    """

    authentication_details = fields.Field()
    performance_de = fields.Dict(
        attribute=api_c.PERFORMANCE_METRICS_DATA_EXTENSION,
        example={
            api_c.NAME: db_c.DELIVERY_PLATFORM_SFMC,
            api_c.DATA_EXTENSION_ID: "5f5f7262997acad4bac4373c",
        },
        required=False,
        allow_none=True,
    )


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

    class Meta:
        """
        set the ordering of facebook auth constants
        """

        ordered = True

    facebook_ad_account_id = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Ad Account ID",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    facebook_app_id = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "App ID",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    facebook_app_secret = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "App Secret",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    facebook_access_token = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Access Token",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )


class SFMCAuthConstants(Schema):
    """
    SFMC Auth constants schema class
    """

    class Meta:
        """
        set the ordering of sfmc.py auth constants
        """

        ordered = True

    sfmc_account_id = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Account ID",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    sfmc_auth_base_uri = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Auth Base URI",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    sfmc_client_id = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Client ID",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    sfmc_client_secret = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Client Secret",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    sfmc_rest_base_uri = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "REST Base URI",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    sfmc_soap_base_uri = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "SOAP Base URI",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )


class DestinationConstantsSchema(Schema):
    """
    Destination constants schema class
    """

    class Meta:
        """
        set the ordering of destination constants
        """

        ordered = True

    facebook = fields.Nested(FacebookAuthConstants)
    salesforce = fields.Nested(SFMCAuthConstants)


class DestinationDataExtPostSchema(Schema):
    """
    Destination data extension post schema class
    """

    data_extension = fields.String()
    type = fields.String()


class DestinationDataExtGetSchema(Schema):
    """
    Destination data extension get schema class
    """

    name = fields.Field(attribute="Name", example="data_extension_name")
    data_extension_id = fields.String(
        attribute="CustomerKey", example="data_extension_id"
    )
