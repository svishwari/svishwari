# pylint: disable=no-self-use
"""
Schemas for the Destinations API
"""

from flask_marshmallow import Schema
from marshmallow import fields, post_load
from marshmallow.validate import OneOf
from bson import ObjectId
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c


class DestinationGetSchema(Schema):
    """
    Destinations schema class
    """

    destination_id = fields.String(
        attribute=api_c.DESTINATION_ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
    )
    destination_type = fields.String(
        attribute=api_c.DESTINATION_TYPE, example="Facebook"
    )
    destination_name = fields.String(
        attribute=api_c.DESTINATION_NAME, example="My destination"
    )
    destination_status = fields.String(
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
    created = fields.DateTime(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = fields.DateTime(attribute=db_c.CREATED_BY, allow_none=True)
    updated = fields.DateTime(attribute=db_c.UPDATED_BY, allow_none=True)
    updated_by = fields.DateTime(attribute=db_c.UPDATE_TIME, allow_none=True)

    @post_load()
    # pylint: disable=unused-argument
    def process_modified(
        self,
        data: dict,
        many: bool = False,
        pass_original=False,
        partial=False,
    ) -> dict:
        """process the schema before deserializing.

        Args:
            data (dict): The destination object
            many (bool): If there are many to process
        Returns:
            Response: Returns a destination object

        """
        # set the input ID to an object ID
        if api_c.DESTINATION_ID in data:
            # if a valid ID, map it
            if ObjectId.is_valid(data[api_c.DESTINATION_ID]):
                data.update(destination_id=ObjectId(data[api_c.DESTINATION_ID]))
            else:
                # otherwise map to None
                data.update(destination_id=None)
        return data


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
