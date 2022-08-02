"""Purpose of this file is for interacting with aws"""
from enum import Enum
import boto3
from huxunifylib.util.general.const import (
    FacebookCredentials,
    SFMCCredentials,
    SendgridCredentials,
    GoogleCredentials,
    QualtricsCredentials,
)

import huxunifylib.database.constants as db_c
from huxunify.api import constants as api_c
from huxunify.api import config
from huxunify.api.data_connectors.cloud.cloud_client import CloudClient


def get_aws_client(
    client: str = "s3",
    region_name: str = config.get_config().AWS_REGION,
) -> boto3.client:
    """quick and dirty function for getting most AWS clients

    Args:
        client (str): client string
        region_name (str): Region Name

    Returns:
        Response: boto3 client

    """
    return boto3.client(
        client,
        region_name=region_name,
    )


def get_auth_from_parameter_store(auth: dict, destination_type: str) -> dict:
    """Get auth details from parameter store

    Args:
        auth (dict): Destination Auth details.
        destination_type (str): Destination type (i.e. facebook, sfmc).

    Returns:
        Auth Object (dict): SFMC auth object.

    Raises:
        KeyError: Exception when the key is missing in the object.
    """

    # only get the secrets from ssm, otherwise take from the auth details.
    if destination_type not in api_c.DESTINATION_SECRETS:
        raise KeyError(
            f"{destination_type} does not have a secret store mapping."
        )

    # pull the secrets from ssm
    for secret in api_c.DESTINATION_SECRETS[destination_type]:
        auth[secret] = CloudClient().get_secret(auth[secret])

    if destination_type == db_c.DELIVERY_PLATFORM_SFMC:
        return {
            SFMCCredentials.SFMC_ACCOUNT_ID.value: auth[api_c.SFMC_ACCOUNT_ID],
            SFMCCredentials.SFMC_AUTH_URL.value: auth[
                api_c.SFMC_AUTH_BASE_URI
            ],
            SFMCCredentials.SFMC_CLIENT_ID.value: auth[api_c.SFMC_CLIENT_ID],
            SFMCCredentials.SFMC_CLIENT_SECRET.value: auth[
                api_c.SFMC_CLIENT_SECRET
            ],
            SFMCCredentials.SFMC_SOAP_ENDPOINT.value: auth[
                api_c.SFMC_SOAP_BASE_URI
            ],
            SFMCCredentials.SFMC_URL.value: auth[api_c.SFMC_REST_BASE_URI],
        }

    if destination_type == db_c.DELIVERY_PLATFORM_FACEBOOK:
        return {
            FacebookCredentials.FACEBOOK_AD_ACCOUNT_ID.name: auth[
                api_c.FACEBOOK_AD_ACCOUNT_ID
            ],
            FacebookCredentials.FACEBOOK_APP_ID.name: auth[
                api_c.FACEBOOK_APP_ID
            ],
            FacebookCredentials.FACEBOOK_APP_SECRET.name: auth[
                api_c.FACEBOOK_APP_SECRET
            ],
            FacebookCredentials.FACEBOOK_ACCESS_TOKEN.name: auth[
                api_c.FACEBOOK_ACCESS_TOKEN
            ],
        }

    if destination_type in [
        db_c.DELIVERY_PLATFORM_SENDGRID,
        db_c.DELIVERY_PLATFORM_TWILIO,
    ]:
        return {
            SendgridCredentials.SENDGRID_AUTH_TOKEN.name: auth[
                api_c.SENDGRID_AUTH_TOKEN
            ],
        }

    if destination_type == db_c.DELIVERY_PLATFORM_QUALTRICS:
        return {
            QualtricsCredentials.QUALTRICS_API_TOKEN.name: auth[
                api_c.QUALTRICS_API_TOKEN
            ],
            QualtricsCredentials.QUALTRICS_DATA_CENTER.name: auth[
                api_c.QUALTRICS_DATA_CENTER
            ],
            QualtricsCredentials.QUALTRICS_OWNER_ID.name: auth[
                api_c.QUALTRICS_OWNER_ID
            ],
            QualtricsCredentials.QUALTRICS_DIRECTORY_ID.name: auth[
                api_c.QUALTRICS_DIRECTORY_ID
            ],
        }

    if destination_type == db_c.DELIVERY_PLATFORM_GOOGLE:
        return {
            GoogleCredentials.GOOGLE_DEVELOPER_TOKEN.name: auth[
                api_c.GOOGLE_DEVELOPER_TOKEN
            ],
            GoogleCredentials.GOOGLE_REFRESH_TOKEN.name: auth[
                api_c.GOOGLE_REFRESH_TOKEN
            ],
            GoogleCredentials.GOOGLE_CLIENT_CUSTOMER_ID.name: auth[
                api_c.GOOGLE_CLIENT_CUSTOMER_ID
            ],
            GoogleCredentials.GOOGLE_CLIENT_ID.name: auth[
                api_c.GOOGLE_CLIENT_ID
            ],
            GoogleCredentials.GOOGLE_CLIENT_SECRET.name: auth[
                api_c.GOOGLE_CLIENT_SECRET
            ],
        }

    return auth


class CloudWatchState(Enum):
    """Define enum for cloud watch states"""

    DISABLE = "disable_rule"
    ENABLE = "enable_rule"
