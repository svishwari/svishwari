"""Module for AWS cloud operations"""
import logging
from typing import Tuple

import boto3
import botocore

from huxunify.api.data_connectors.cloud.cloud_client import (
    CloudClient,
)
import huxunify.api.constants as api_c
from huxunify.api.config import get_config, Config

# pylint: disable=missing-raises-doc
from huxunify.api.prometheus import record_health_status_metric


class AWSClient(CloudClient):
    """Class for AWS cloud operations"""

    provider = "aws"

    def __init__(self, config: Config = get_config()):
        """Instantiate the AWS client class"""
        super().__init__(config)

    # pylint: disable=no-self-use
    def get_aws_client(
        self,
        client: str = "s3",
        region_name: str = "",
    ) -> boto3.client:
        """Retrieves AWS client.
        (Most of them)

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

    def get_secret(self, secret_name: str, **kwargs) -> str:
        """Retrieve secret from AWS Parameter Store.

        Args:
            secret_name (str): Name of the secret.
            **kwargs (dict): function keyword arguments.

        Returns:
            str: The value of the secret.
        """
        try:
            return (
                self.get_aws_client(api_c.AWS_SSM_NAME, self.config.AWS_REGION)
                .get_parameter(
                    Name=secret_name,
                    WithDecryption=True,
                )
                .get("Parameter")
                .get("Value")
            )
        except botocore.exceptions.ClientError as error:
            logging.error(
                "Failed to get %s from AWS parameter store.", secret_name
            )
            raise error

    def set_secret(self, secret_name: str, value: str, **kwargs) -> None:
        """Set the secret in AWS Parameter Store.

        Args:
            secret_name (str): Name of the secret.
            value (str): The value of the secret.
            **kwargs (dict): function keyword arguments.

        Returns:
        """
        try:
            self.get_aws_client(api_c.AWS_SSM_NAME).put_parameter(
                Name=secret_name,
                Value=value,
                Type="SecureString",
                Overwrite=False,
            )
        except Exception as exc:
            logging.error(
                "Failed to set %s in AWS parameter store.", secret_name
            )
            raise exc

    def upload_file(
        self, file_name: str, file_type: str, user_name: str, **kwargs
    ) -> bool:
        """Upload a file to AWS S3.

        Args:
            file_name (str): Name of the file to upload.
            file_type (str): Type of the file to upload.
            user_name (str): Name of the user uploading the file.
            **kwargs (dict): function keyword arguments.

        Returns:

        """
        raise NotImplementedError()

    def download_file(self, file_name: str, user_name: str, **kwargs) -> bool:
        """Download a file from AWS S3.

        Args:
            file_name (str): Name of the file to upload.
            user_name (str): Name of the user uploading the file.
            **kwargs (dict): function keyword arguments.

        Returns:
            bool: indication that download was successful.
        """
        raise NotImplementedError()

    def __check_aws_health_connection(
        self, client_method: str, extra_params: dict, client: str = "s3"
    ):
        """Validate an AWS service connection.

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
            getattr(self.get_aws_client(client), client_method)(**extra_params)
            return True, f"{client} available."
        except Exception as exception:  # pylint: disable=broad-except
            # report the generic error message
            return False, getattr(exception, "message", repr(exception))

    def health_check_batch_service(self) -> Tuple[bool, str]:
        """Checks the health of the AWS batch service.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        status = self.__check_aws_health_connection(
            client_method="cancel_job",
            client=api_c.AWS_BATCH_NAME,
            extra_params={"jobId": "test", "reason": "test"},
        )
        record_health_status_metric(
            api_c.AWS_BATCH_CONNECTION_HEALTH, status[0]
        )
        return status

    def health_check_storage_service(self) -> Tuple[bool, str]:
        """Checks the health of the AWS storage service.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        status = self.__check_aws_health_connection(
            client_method="get_bucket_location",
            client=api_c.AWS_S3_NAME,
            extra_params={api_c.AWS_BUCKET: self.config.S3_DATASET_BUCKET},
        )
        record_health_status_metric(api_c.AWS_S3_CONNECTION_HEALTH, status[0])
        return status
