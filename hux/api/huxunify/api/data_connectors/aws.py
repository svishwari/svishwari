"""
purpose of this file is for interacting with aws
"""
from os import getenv
from http import HTTPStatus
from connexion import ProblemException
import boto3
import botocore
from huxunify.api import constants as api_c


# TODO - HUS-281
# get aws connection params
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = getenv("AWS_REGION")
AWS_SERVICE_URL = getenv("AWS_SERVICE_URL")
SSM_NAME = "ssm"


class ParameterStore:
    """Interact with AWS Parameter Store."""

    @staticmethod
    def store_secret(
        name: str,
        secret: str,
        overwrite: bool,
        path: str = None,
    ) -> dict:
        """Store secrets.

        Args:
            name (str): Name of the parameter.
            secret (str): The parameter value that you want to add to the store.
            overwrite (bool): Overwrite an existing parameter.
            path (str): Hierarchy of the parameter. (e.g: /Dev/DBServer/MySQL/db-string13)
        Returns:
            dict: boto3 response.
        """
        try:
            return get_aws_client(SSM_NAME).put_parameter(
                Name=f"{path}/{name}" if path else name,
                Value=secret,
                Type="SecureString",
                Overwrite=overwrite,
            )
        except botocore.exceptions.ClientError as error:
            raise error

    @staticmethod
    def get_store_value(
        name: str, path: str = None, value: str = "Value"
    ) -> str:
        """
        Retrieve a parameter/value from the param store.

        Args:
            name (str): Name of the parameter.
            path (str): Hierarchy of the parameter. (e.g: /Dev/DBServer/MySQL/db-string13)
            value (str): Name of the value to get (i.e. Name or Value)
        Returns:
            str: Parameter Value.
        """
        try:
            return (
                get_aws_client(SSM_NAME)
                .get_parameter(
                    Name=f"{path}/{name}" if path else name,
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
        destination_name: str,
    ) -> dict:
        """Save authentication details in AWS Parameter Store.

        Args:
            authentication_details (dict): The key/secret pair to store away.
            is_updated (bool): Flag to update the secrets in the AWS Parameter Store.
            destination_id (str): destinations ID.
            destination_name (str): destinations name.

        Returns:
            ssm_params (dict): The key/path to where the parameters are stored.
        """
        ssm_params = {}
        path = f"/{api_c.PARAM_STORE_PREFIX}/{destination_id}"

        for (
            parameter_name,
            secret,
        ) in authentication_details.items():
            ssm_params[parameter_name] = (
                f"{path}/{parameter_name}" if path else parameter_name
            )
            try:
                parameter_store.store_secret(
                    name=parameter_name,
                    secret=secret,
                    overwrite=is_updated,
                    path=path,
                )
            except botocore.exceptions.ClientError as exc:
                raise ProblemException(
                    status=int(HTTPStatus.BAD_REQUEST.value),
                    title=HTTPStatus.BAD_REQUEST.description,
                    detail=f"{api_c.PARAMETER_STORE_ERROR_MSG}"
                    f" destination_name: {destination_name}.",
                ) from exc

        return ssm_params


parameter_store = ParameterStore()


def get_aws_client(
    client: str = "s3",
    aws_access_key: str = AWS_ACCESS_KEY_ID,
    aws_secret_key: str = AWS_SECRET_ACCESS_KEY,
    region_name: str = AWS_REGION,
) -> boto3.client:
    """quick and dirty function for getting most AWS clients

    Args:
        client (str): client string
        aws_access_key (str): AWS access key
        aws_secret_key (str): AWS secret key
        region_name (str): Region Name

    Returns:
        Response: boto3 client

    """
    return boto3.client(
        client,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name,
    )
