"""
purpose of this file is for interacting with aws
"""
from typing import Tuple
from http import HTTPStatus
from connexion import ProblemException
import boto3
import botocore
from huxunify.api import constants as api_c
from huxunify.api import config


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
        """
        Retrieve a parameter/value from the param store.

        Args:
            name (str): Name of the parameter.
            value (str): Name of the value to get (i.e. Name or Value)
        Returns:
            str: Parameter Value.
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
                not in api_c.DESTINATION_SECRETS[destination_type]
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


def check_aws_connection(client="s3") -> Tuple[bool, str]:
    """Validate an AWS connection.

    Args:
        client (str): name of the boto3 client to use.
    Returns:
        tuple[bool, str]: Returns if the AWS connection is valid,
            and the message.
    """

    try:
        # lookup the health test to run from api constants
        health_test = api_c.AWS_HEALTH_TESTS[client]
        getattr(get_aws_client(client), health_test[0])(**health_test[1])
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
    return check_aws_connection(api_c.AWS_SSM_NAME)


def check_aws_batch() -> Tuple[bool, str]:
    """Validate AWS batch Function

    Returns:
        tuple[bool, str]: Returns if the AWS connection is valid,
            and the message.
    """
    return check_aws_connection(api_c.AWS_BATCH_NAME)
