"""Purpose of this file is for interacting with aws"""
import logging
import os
from typing import Tuple
from enum import Enum
from http import HTTPStatus

from connexion import ProblemException
import boto3
import botocore
from bson import ObjectId
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
from huxunify.api.prometheus import record_health_status_metric


class ParameterStore:
    """Interact with AWS Parameter Store."""

    @staticmethod
    def store_secret(name: str, secret: str, overwrite: bool) -> dict:
        """Store secrets.

        Args:
            name (str): Name of the parameter.
            secret (str): The parameter value that you want to add to the store.
            overwrite (bool): Overwrite an existing parameter.
        Returns:
            dict: boto3 response.
        Raises:
            ClientError: Boto client request error.
        """
        try:
            return get_aws_client(api_c.AWS_SSM_NAME).put_parameter(
                Name=name,
                Value=secret,
                Type="SecureString",
                Overwrite=overwrite,
            )
        except botocore.exceptions.ClientError as error:
            raise error

    @staticmethod
    def get_store_value(name: str, value: str = "Value") -> str:
        """Retrieve a parameter/value from the param store.

        Args:
            name (str): Name of the parameter.
            value (str): Name of the value to get (i.e. Name or Value)
        Returns:
            str: Parameter Value.
        Raises:
            ClientError: Boto client request error.
        """
        try:
            return (
                get_aws_client(api_c.AWS_SSM_NAME)
                .get_parameter(
                    Name=name,
                    WithDecryption=True,
                )
                .get("Parameter")
                .get(value)
            )
        except botocore.exceptions.ClientError as error:
            raise error

    @staticmethod
    def set_destination_authentication_secrets(
        authentication_details: dict,
        is_updated: bool,
        destination_id: str,
        destination_type: str,
    ) -> dict:
        """Save authentication details in AWS Parameter Store.

        Args:
            authentication_details (dict): The key/secret pair to store away.
            is_updated (bool): Flag to update the secrets in the AWS Parameter Store.
            destination_id (str): destinations ID.
            destination_type (str): destination type (i.e. facebook, sfmc)

        Returns:
            ssm_params (dict): The key to where the parameters are stored.
        Raises:
            KeyError: Exception when the key is missing in the object.
            ProblemException: Any exception raised during endpoint execution.
        """
        ssm_params = {}

        if destination_type not in api_c.DESTINATION_SECRETS:
            raise KeyError(
                f"{destination_type} does not have a secret store mapping."
            )

        for (
            parameter_name,
            secret,
        ) in authentication_details.items():

            # only store secrets in ssm, otherwise store in object.
            if (
                parameter_name
                in api_c.DESTINATION_SECRETS[destination_type][api_c.MONGO]
            ):
                ssm_params[parameter_name] = secret
                continue

            param_name = f"{api_c.PARAM_STORE_PREFIX}_{parameter_name}"
            ssm_params[parameter_name] = param_name
            try:
                parameter_store.store_secret(
                    name=param_name,
                    secret=secret,
                    overwrite=is_updated,
                )
            except botocore.exceptions.ClientError as exc:
                raise ProblemException(
                    status=int(HTTPStatus.BAD_REQUEST.value),
                    title=HTTPStatus.BAD_REQUEST.description,
                    detail=f"{api_c.PARAMETER_STORE_ERROR_MSG}"
                    f" destination_id: {destination_id}.",
                ) from exc

        return ssm_params


parameter_store = ParameterStore()


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


def check_aws_connection(
    client_method: str, extra_params: dict, client: str = "s3"
) -> Tuple[bool, str]:
    """Validate an AWS connection.

    Args:
        client_method (str): Method name for the client
        extra_params (dict): Extra params required for aws connection
        client (str): name of the boto3 client to use.
    Returns:
        tuple[bool, str]: Returns if the AWS connection is valid,
            and the message.
    """

    try:
        # lookup the health test to run from api constants
        getattr(get_aws_client(client), client_method)(**extra_params)
        return True, f"{client} available."
    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        return False, getattr(exception, "message", repr(exception))


def check_aws_ssm() -> Tuple[bool, str]:
    """Validate AWS ssm Function

    Returns:
        tuple[bool, str]: Returns if the AWS connection is valid,
            and the message.
    """
    status = check_aws_connection(
        client_method="get_parameter",
        client=api_c.AWS_SSM_NAME,
        extra_params={"Name": "unifieddb_host_alias"},
    )
    record_health_status_metric(api_c.AWS_SSM_CONNECTION_HEALTH, status[0])
    return status


def check_aws_batch() -> Tuple[bool, str]:
    """Validate AWS batch Function

    Returns:
        tuple[bool, str]: Returns if the AWS connection is valid,
            and the message.
    """
    status = check_aws_connection(
        client_method="cancel_job",
        client=api_c.AWS_BATCH_NAME,
        extra_params={"jobId": "test", "reason": "test"},
    )
    record_health_status_metric(api_c.AWS_BATCH_CONNECTION_HEALTH, status[0])
    return status


def check_aws_s3() -> Tuple[bool, str]:
    """Validate AWS S3 Function

    Returns:
        tuple[bool, str]: Returns if the AWS connection is valid,
            and the message.

    """
    status = check_aws_connection(
        client_method="get_bucket_location",
        client=api_c.AWS_S3_NAME,
        extra_params={api_c.AWS_BUCKET: config.get_config().S3_DATASET_BUCKET},
    )
    record_health_status_metric(api_c.AWS_S3_CONNECTION_HEALTH, status[0])
    return status


def check_aws_events() -> Tuple[bool, str]:
    """Validates AWS events function

    Returns:
        tuple[bool, str]: Returns if the AWS connection is valid,
            and the message.
    """
    status = check_aws_connection(
        client_method="put_rule",
        client=api_c.AWS_EVENTS_NAME,
        extra_params={
            "Name": "unified_health_check",
            "State": "DISABLED",
            "Description": "test health check",
            "RoleArn": config.get_config().AUDIENCE_ROUTER_JOB_ROLE_ARN,
            "ScheduleExpression": "cron(15 0 * * ? *)",
        },
    )
    record_health_status_metric(api_c.AWS_EVENTS_CONNECTION_HEALTH, status[0])
    return status


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
    for secret in api_c.DESTINATION_SECRETS[destination_type][
        api_c.AWS_SSM_NAME
    ]:
        auth[secret] = parameter_store.get_store_value(auth[secret])

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


def set_cloud_watch_rule(
    rule_name: str,
    schedule_expression: str,
    role_arn: str,
    description: str = "",
    state: str = api_c.ENABLED,
) -> str:
    """Create or Update a cloud watch rule

    Args:
        rule_name (str): name of the rule you are creating or updating.
        schedule_expression (str): The scheduling expression.
            For example "cron(0 20 * * ? *)" or "rate(5 minutes)".
        role_arn (str): The Amazon resource name (ARN) of the IAM role
            associated with the rule.
        description (str): A description of the rule.
        state (str): Indicates whether the rule is enabled or disabled.

    Returns:
        rule_arn (str): The Amazon resource name (ARN) of the rule.

    Raises:
        ValueError: Error indicating unsupported values.
    """

    if state.upper() not in [api_c.ENABLED.upper(), api_c.DISABLED.upper()]:
        raise ValueError(f"Invalid state provided {state}")

    if " " in rule_name:
        raise ValueError(f"Unsupported spaces in rule name {rule_name}")

    try:
        aws_events = get_aws_client(api_c.AWS_EVENTS_NAME)
        response = aws_events.put_rule(
            Name=rule_name,
            ScheduleExpression=schedule_expression,
            State=state.upper(),
            Description=description,
            RoleArn=role_arn,
        )

        # validate successful creation
        if (
            response["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.OK.value
        ):
            logging.error(
                "Failed to create event %s: client error.", rule_name
            )
            return None

        # return the request id
        return response["RuleArn"]

    # pylint: disable=broad-except
    except Exception as exception:
        logging.error("Failed to create event %s: %s", rule_name, exception)
        return None


def put_rule_targets_aws_batch(
    rule_name: str,
    batch_params: dict,
    delivery_job_id: ObjectId,
    role_arn: str,
    job_queue: str,
) -> str:
    """Adds the specified targets to the specified rule or updates
    the targets if they are already associated with the rule.

    Args:
        rule_name (str): name of the rule you are creating or updating.
        batch_params (dict): Batch parameter dict for all batch job params.
        delivery_job_id (ObjectId): Delivery Job Id.
        role_arn (str): The Amazon resource name of the IAM role to be used
            for this target and when the rule is triggered.
        job_queue (str): The Batch Job queue.

    Returns:
        event request id (str): The Amazon resource name (ARN) of the rule.
    """

    try:
        # get the aws client
        aws_events = get_aws_client(api_c.AWS_EVENTS_NAME)

        # put the batch job targets
        response = aws_events.put_targets(
            Rule=rule_name,
            Targets=[
                {
                    api_c.AWS_TARGET_ID: str(delivery_job_id),
                    api_c.AWS_TARGET_ARN: job_queue,
                    api_c.AWS_TARGET_ROLE_ARN: role_arn,
                    api_c.AWS_TARGET_BATCH_PARAMS: batch_params,
                }
            ],
        )

        # validate successful creation
        if (
            response["ResponseMetadata"]["HTTPStatusCode"]
            == HTTPStatus.OK.value
        ):
            # return the request id
            return response["FailedEntryCount"]

        error_msg = f"Failed to put target for {rule_name}: client error."
        logging.error(error_msg)
        return None

    # pylint: disable=broad-except
    except Exception as exception:
        logging.error("Failed to put target for %s: %s", rule_name, exception)
        return None


class CloudWatchState(Enum):
    """Define enum for cloud watch states"""

    DISABLE = "disable_rule"
    ENABLE = "enable_rule"


def toggle_cloud_watch_rule(
    rule_name: str, state: CloudWatchState, ignore_existence: bool = True
) -> None:
    """Enable or Disable Cloud watch rule.

    Args:
        rule_name (str): Name of the rule you are creating or updating.
        state (CloudWatchState): Toggle state of the cloud watch rule.
        ignore_existence (bool): Cloud watch fails if the rules does not exist.
            Toggle regardless of checking existence.

    Returns:
        bool: exception was handled, return false.

    Raises:
        ClientError: Boto client request error.

    """

    try:
        aws_events = get_aws_client(api_c.AWS_EVENTS_NAME)
        response = getattr(aws_events, state.value)(Name=rule_name)

        # validate successful creation
        success = (
            response["ResponseMetadata"]["HTTPStatusCode"]
            == HTTPStatus.OK.value
        )
        if not success:
            logging.error("Failed to create toggle %s.", rule_name)
        return success

    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ResourceNotFoundException":
            logging.error("Resource not found %s.", rule_name)
            if not ignore_existence:
                raise error
        else:
            logging.error("Unexpected client error %s.", rule_name)

    except Exception as exception:  # pylint:disable=broad-except
        logging.error("Failed to create event %s: %s", rule_name, exception)

    # exception was handled, return false.
    return False


def upload_file(
    file_name: str,
    bucket: str,
    object_name: str = None,
    user_name: str = None,
    file_type: str = None,
) -> bool:
    """Upload a file to an S3 bucket

    Args:
        file_name (str): Path to file object
        bucket (str): S3 bucket name
        object_name (str): S3 object name, defaulting to None
        user_name (str): User name
        file_type (str): File type
    Returns:
        bool: True for successful upload else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = get_aws_client(api_c.AWS_S3_NAME)

    extraargs = {
        "Metadata": {
            api_c.CREATED_BY: user_name if user_name else "",
            api_c.TYPE: file_type if file_type else "",
        }
    }
    logging.info("Uploading %s file to %s", file_name, bucket)
    try:
        _ = s3_client.upload_file(file_name, bucket, object_name, extraargs)

    except botocore.exceptions.ClientError as exception:
        logging.error(
            "Failed to upload file %s to %s : %s", file_name, bucket, exception
        )
        return False
    logging.info("Uploaded %s file to %s", file_name, bucket)
    return True


def download_file(
    bucket: str, file_name: str, object_name: str = None
) -> bool:
    """Downloads a file from S3 bucket

    Args:
        bucket (str): S3 bucket name
        file_name (str): File mame
        object_name (str): Object name

    Returns:
        bool: True for successful download else False
    """
    object_name = object_name if object_name else file_name
    s3_client = get_aws_client(api_c.AWS_S3_NAME)
    logging.info("Downloading %s file to %s", file_name, bucket)
    try:
        with open(file_name, "wb") as file:
            s3_client.download_fileobj(bucket, object_name, file)
    except botocore.exceptions.ClientError as exception:
        logging.error(
            "Failed to download file object %s from %s : %s",
            object_name,
            bucket,
            exception,
        )
        return False
    logging.info("Downloaded %s file from %s", file_name, bucket)
    return True


# if __name__ == "__main__":
#     return check_aws_connection(
#         client_method="get_parameter",
#         client=api_c.AWS_SSM_NAME,
#         extra_params={"Name": "unifieddb_host_alias"},
#     )
