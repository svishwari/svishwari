"""
purpose of this file is for interacting with aws
"""
from os import getenv
from http import HTTPStatus
from connexion import ProblemException
import boto3
import botocore


# TODO - HUS-281
# get aws connection params
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = getenv("AWS_REGION")
AWS_SERVICE_URL = getenv("AWS_SERVICE_URL")
SSM_NAME = "ssm"
PARAM_STORE_PREFIX = "huxunify"
PARAM_STORE_ERROR_MSG = (
    "There was a problem saving your authentication details for "
    "destinations: '{destination_name}'. Details: Trouble storing secrets in the "
    "parameter store"
)


class ParameterStore:
    """Interact with AWS Parameter Store."""

    @staticmethod
    def get_ssm_client() -> boto3.client:
        """Get the SSM client

        Args:
        Returns:
            boto3.client: a boto3 client.
        """
        return boto3.client(
            SSM_NAME,
            region_name=AWS_REGION,
            endpoint_url=AWS_SERVICE_URL,
        )

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
            return (
                ParameterStore()
                .get_ssm_client()
                .put_parameter(
                    Name=f"{path}/{name}" if path else name,
                    Value=secret,
                    Type="SecureString",
                    Overwrite=overwrite,
                )
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
                ParameterStore()
                .get_ssm_client()
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
        path = f"/{PARAM_STORE_PREFIX}/{destination_id}"

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
                    detail=PARAM_STORE_ERROR_MSG.format(
                        destination_name=destination_name
                    ),
                ) from exc

        return ssm_params


parameter_store = ParameterStore()


def get_aws_client(
    client="s3",
    aws_access_key=AWS_ACCESS_KEY_ID,
    aws_secret_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
):
    """
    quick and dirty function for getting most AWS clients
    :param client:
    :param resource:
    :param aws_access_key:
    :param aws_secret_key:
    :param region_name:
    :return: aws client
    """
    return boto3.client(
        client,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name,
    )
