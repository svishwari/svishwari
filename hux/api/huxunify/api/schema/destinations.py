# pylint: disable=no-self-use
"""Schemas for the Destinations API"""
from flask_marshmallow import Schema
from marshmallow import fields, pre_load, ValidationError
from marshmallow.validate import OneOf, Range, Equal
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import (
    must_not_be_blank,
    validate_object_id,
)
from huxunify.api.schema.custom_schemas import DateTimeWithZ


class DataExtensionSchema(Schema):
    """Engagement Audience Destination Data Extension Schema"""

    data_extension_name = fields.String()


class DestinationDataExtSchema(Schema):
    """Destination data extension schema class"""

    name = fields.String(example="data_extension_name")
    data_extension_id = fields.String(example="data_extension_id")


class DeliveryScheduleDailySchema(Schema):
    """Delivery Schedule Daily schema class"""

    periodicity = fields.String(
        default=api_c.DAILY, validate=Equal(api_c.DAILY)
    )
    every = fields.Int(example=2, validate=Range(min=1, max=7))
    hour = fields.Int(example=11, validate=Range(min=1, max=12))
    minute = fields.Int(example=15, validate=Range(min=0, max=59))
    period = fields.String(
        example=api_c.AM,
        validate=[OneOf(choices=[api_c.AM, api_c.PM])],
    )


class DeliveryScheduleWeeklySchema(DeliveryScheduleDailySchema):
    """Delivery Schedule Weekly schema class"""

    periodicity = fields.String(
        default=api_c.WEEKLY, validate=Equal(api_c.WEEKLY)
    )
    every = fields.Int(example=2, validate=Range(min=1, max=4))
    day_of_week = fields.List(
        fields.String(
            required=True,
            validate=OneOf(api_c.DAY_LIST),
        ),
    )


class DeliveryScheduleMonthlySchema(DeliveryScheduleDailySchema):
    """Delivery Schedule Monthly schema class"""

    periodicity = fields.String(
        default=api_c.MONTHLY, validate=Equal(api_c.MONTHLY)
    )
    every = fields.Int(example=2, validate=Range(min=1, max=12))
    monthly_period_items = fields.List(
        fields.String(
            required=True,
            validate=OneOf(api_c.MONTHLY_PERIOD_LIST),
        ),
    )
    day_of_month = fields.List(
        fields.String(
            required=True,
            validate=OneOf(api_c.DAY_OF_MONTH_LIST),
        ),
    )


class DeliveryScheduleSchema(Schema):
    """Generalized Delivery Schedule Schema"""

    periodicity = fields.String(example=api_c.DAILY, required=True)
    every = fields.Int(example=2)
    minute = fields.Int(example=15, validate=Range(min=0, max=45))
    hour = fields.Int(example=11, validate=Range(min=1, max=12))
    period = fields.String(
        example=api_c.AM,
        validate=[OneOf(choices=[api_c.AM, api_c.PM])],
    )
    day_of_week = fields.List(
        fields.String(
            required=True,
            validate=OneOf(api_c.DAY_LIST),
        ),
    )
    monthly_period_items = fields.List(
        fields.String(
            required=True,
            validate=OneOf(api_c.MONTHLY_PERIOD_LIST),
        ),
    )
    day_of_month = fields.List(
        fields.String(
            required=True,
            validate=OneOf(api_c.DAY_OF_MONTH_LIST),
        ),
    )

    @pre_load
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def unwrap_envelope(self, data: dict, **kwargs) -> dict:
        """Validates delivery schedule as daily, monthly and weekly.

        Args:
            data(dict): Data passed to schema.
            **kwargs (dict): Key word args.
        Returns:
            data: Data after validation, modification.
        Raises:
            ValidationError: Error for improperly formatted delivery schedule

        """
        if data.get(api_c.PERIODICIY) == api_c.DAILY:
            DeliveryScheduleDailySchema().validate(api_c.DAILY)
        elif data.get(api_c.PERIODICIY) == api_c.MONTHLY:
            # convert list of integers to string.
            data[api_c.DAY_OF_MONTH] = [
                str(x) for x in data.get(api_c.DAY_OF_MONTH, [])
            ]
            DeliveryScheduleMonthlySchema().validate(api_c.MONTHLY)
        elif data.get(api_c.PERIODICIY) == api_c.WEEKLY:
            DeliveryScheduleWeeklySchema().validate(api_c.WEEKLY)
        else:
            raise ValidationError(
                "Delivery Schedule does not conform with "
                f"either {api_c.DAILY}, {api_c.MONTHLY}, "
                f"{api_c.WEEKLY} schemas."
            )

        return data


class DestinationDataExtConfigSchema(Schema):
    """Destination data extension configuration schema class"""

    performance_metrics_data_extension = fields.Nested(
        DestinationDataExtSchema, required=True
    )
    campaign_activity_data_extension = fields.Nested(
        DestinationDataExtSchema, required=True
    )


class DestinationGetSchema(Schema):
    """Destinations get schema class"""

    _id = fields.String(
        data_key=api_c.ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    type = fields.String(
        attribute=api_c.DELIVERY_PLATFORM_TYPE,
        example=db_c.DELIVERY_PLATFORM_SFMC,
    )
    name = fields.String(
        attribute=api_c.DESTINATION_NAME,
        example=db_c.DELIVERY_PLATFORM_SFMC.title(),
    )
    status = fields.String(
        attribute=api_c.CONNECTION_STATUS,
        validate=[
            OneOf(
                choices=[
                    api_c.STATUS_NOT_DELIVERED,
                    api_c.STATUS_DELIVERING,
                    api_c.STATUS_DELIVERED,
                    api_c.STATUS_DELIVERY_PAUSED,
                    api_c.STATUS_ACTIVE,
                    api_c.STATUS_PENDING,
                    api_c.STATUS_ERROR,
                    api_c.STATUS_REQUESTED,
                ]
            )
        ],
    )
    category = fields.String(attribute=db_c.CATEGORY, example=db_c.ADVERTISING)
    campaigns = fields.Int(
        attribute=api_c.DESTINATION_CAMPAIGN_COUNT, example=5, read_only=True
    )
    configuration = fields.Nested(
        DestinationDataExtConfigSchema, required=False, allow_none=True
    )
    is_added = fields.Bool(attribute="added")
    is_enabled = fields.Bool(attribute="enabled")
    is_ad_platform = fields.Bool(attribute=db_c.IS_AD_PLATFORM)
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = fields.String(attribute=db_c.CREATED_BY, allow_none=True)
    update_time = DateTimeWithZ(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = fields.String(attribute=db_c.UPDATED_BY, allow_none=True)
    delivery_platform_config = fields.Nested(DataExtensionSchema)
    data_added = DateTimeWithZ(allow_none=True)


class DestinationPatchSchema(Schema):
    """Destinations Patch schema class"""

    type = fields.String(
        attribute=api_c.DELIVERY_PLATFORM_TYPE,
        example=db_c.DELIVERY_PLATFORM_SFMC,
    )
    name = fields.String(
        attribute=api_c.DESTINATION_NAME,
        example=db_c.DELIVERY_PLATFORM_SFMC.title(),
    )
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
                    api_c.REQUESTED,
                ]
            )
        ],
    )
    added = fields.Bool(attribute="added")
    enabled = fields.Bool(attribute="enabled")
    ad_platform = fields.Bool(attribute=db_c.IS_AD_PLATFORM)


class DestinationRequestSchema(Schema):
    """Destinations Request schema class"""

    name = fields.String(
        attribute=api_c.DESTINATION_NAME,
        example="Salesforce Marketing Cloud",
    )
    contact_email = fields.Email(required=False, default=False)
    client_request = fields.Bool(required=False, default=False)
    client_account = fields.Bool(required=False, default=False)
    use_case = fields.String(required=False, allow_none=True)


class DestinationPutSchema(Schema):
    """Destination put schema class"""

    authentication_details = fields.Field()
    configuration = fields.Nested(
        DestinationDataExtConfigSchema, required=False
    )


class DestinationValidationSchema(Schema):
    """Destination validation schema class"""

    authentication_details = fields.Field()
    type = fields.String()


class FacebookAuthConstants(Schema):
    """Facebook Auth constants schema class"""

    class Meta:
        """Set the ordering of facebook auth constants"""

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


class FacebookAuthCredsSchema(Schema):
    """Facebook Auth Credentials schema class"""

    facebook_ad_account_id = fields.String(
        required=True,
        example="MkU3Ojgwm",
    )
    facebook_app_id = fields.String(
        required=True,
        example="717bdOQqZO99",
    )
    facebook_app_secret = fields.String(
        required=True,
        example="2951925002021888",
    )
    facebook_access_token = fields.String(
        required=True,
        example="111333777",
    )


class SFMCAuthConstants(Schema):
    """SFMC Auth constants schema class"""

    class Meta:
        """Set the ordering of sfmc auth constants"""

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


class SFMCAuthCredsSchema(Schema):
    """SFMC Auth Credentials schema class"""

    sfmc_account_id = fields.String(
        required=True,
        example="7329755",
    )
    sfmc_auth_base_uri = fields.String(
        required=True,
        example="https://gsafkhljwhp6798.auth.marketingcloudapis.com/",
    )
    sfmc_client_id = fields.String(
        required=True,
        example="e488010196d046f5a8b1b80ba6100899",
    )
    sfmc_client_secret = fields.String(
        required=True,
        example="4d2c582ab302437c80721c0ec46a30f2",
    )
    sfmc_rest_base_uri = fields.String(
        required=True,
        example="https://535cf647a34-7950b5a4.rest.marketingcloudapis.com/",
    )
    sfmc_soap_base_uri = fields.String(
        required=True,
        example="https://55c5487a374-723ab5a6.soap.marketingcloudapis.com/",
    )


class SendgridAuthCredsSchema(Schema):
    """Sendgrid Auth Credentials schema class"""

    sendgrid_auth_token = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="wue812x2813eyqshjsdbw",
    )


class SendgridAuthConstants(Schema):
    """Sendgrid Auth constants schema class"""

    class Meta:
        """Set the ordering of sendgrid auth constants"""

        ordered = True

    sendgrid_auth_token = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Auth Token",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )


class GoogleAdsAuthCredsSchema(Schema):
    """Google Ads Auth Credentials schema class"""

    google_developer_token = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="dZ%z4Mt4UY=7L6?jSanGsS",
    )
    google_refresh_token = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="Z8BOWqt^PKVVNl&uOoQcL7",
    )
    google_client_customer_id = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="527-056-0438",
    )
    google_client_id = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="ChM263kbF!f.apps.googleusercontent.com",
    )
    google_client_secret = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="Gbh+@gUzVc658Ry=6kgw@_Bx",
    )


class GoogleAdsAuthConstants(Schema):
    """Google Ads Auth constants schema class"""

    class Meta:
        """Set the ordering of google ads auth constants"""

        ordered = True

    google_developer_token = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Google Developer Token",
            api_c.TYPE: "password",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    google_refresh_token = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Google Refresh Token",
            api_c.TYPE: "password",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    google_client_customer_id = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Google Client Customer ID",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    google_client_id = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Google Client ID",
            api_c.TYPE: "password",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )
    google_client_secret = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Google Client Secret",
            api_c.TYPE: "password",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )


class QualtricsAuthCredsSchema(Schema):
    """Qualtrics Auth Credentials schema class"""

    qualtrics_api_token = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="wue812x2813eyqshjsdbw",
    )
    qualtrics_data_center = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="feiwygfewyfgiuqef",
    )
    qualtrics_owner_id = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="kjeahfhb81322132qef",
    )
    qualtrics_directory_id = fields.String(
        required=True,
        validate=must_not_be_blank,
        example="qwjdqwu73176432nfkd",
    )


class QualtricsAuthConstants(Schema):
    """Qualtrics Auth constants schema class"""

    class Meta:
        """Set the ordering of qualtrics auth constants"""

        ordered = True

    qualtrics_api_token = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "API Token",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )

    qualtrics_data_center = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Data Center",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )

    qualtrics_owner_id = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Owner ID",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )

    qualtrics_directory_id = fields.Dict(
        required=True,
        validate=must_not_be_blank,
        example={
            api_c.NAME: "Directory ID",
            api_c.TYPE: "text",
            api_c.REQUIRED: True,
            api_c.DESCRIPTION: None,
        },
    )


class DestinationConstantsSchema(Schema):
    """Destination constants schema class"""

    class Meta:
        """Set the ordering of destination constants"""

        ordered = True

    facebook = fields.Nested(FacebookAuthConstants)
    sfmc = fields.Nested(SFMCAuthConstants)
    sendgrid = fields.Nested(SendgridAuthConstants)
    google_ads = fields.Nested(GoogleAdsAuthConstants)
    qualtrics = fields.Nested(QualtricsAuthConstants)


class DestinationDataExtPostSchema(Schema):
    """Destination data extension post schema class"""

    data_extension = fields.String()
    type = fields.String()


class DestinationDataExtGetSchema(Schema):
    """Destination data extension get schema class"""

    name = fields.String(attribute="Name", example="data_extension_name")
    data_extension_id = fields.String(
        attribute="CustomerKey", example="data_extension_id"
    )
    create_time = DateTimeWithZ(
        attribute="createdDate", required=False, default=None, allow_none=True
    )
