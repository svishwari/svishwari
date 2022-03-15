"""Module for AWS cloud operations"""
import logging
from typing import Tuple
from enum import Enum

import boto3
from botocore.exceptions import ClientError

from huxunify.api.data_connectors.cloud.cloud_client import (
    CloudClient,
)
from huxunify.api.config import get_config, Config


class ClientType(Enum):
    """Holds client types for the boto3 clients"""
    SSM = "ssm"
    S3 = "s3"
    BATCH = "batch"


class AWSClient(CloudClient):
    """Class for AWS cloud operations"""

    provider = "aws"

    def __init__(self, config: Config = get_config()):
        """Instantiate the AWS client class"""
        super().__init__(config)

    # pylint: disable=no-self-use
    def get_aws_client(
        self,
        client_type: ClientType
    ) -> boto3.client:
        """Retrieves AWS client.
        (Most of them)

        Args:
            client_type (ClientType): client type.

        Returns:
            Response: boto3 client

        """
        return boto3.client(
            client_type.value,
            region_name=self.config.AWS_REGION,
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
                self.get_aws_client(ClientType.SSM)
                .get_parameter(
                    Name=secret_name,
                    WithDecryption=True,
                )
                .get("Parameter")
                .get("Value")
            )
        except ClientError as error:
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
            self.get_aws_client(ClientType.SSM).put_parameter(
                Name=secret_name,
                Value=value,
                Type="SecureString",
                Overwrite=False,
            )
        except ClientError as error:
            logging.error(
                "Failed to set %s in AWS parameter store.", secret_name
            )
            raise error

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

    def health_check_batch_service(self) -> Tuple[bool, str]:
        """Checks the health of the AWS batch service.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        try:
            resp = self.get_aws_client(ClientType.BATCH).list_scheduling_policies()
            valid_session = resp["ResponseMetadata"]["HTTPStatusCode"] == 200
            if valid_session:
                return True, "AWS Batch service available."
        except ClientError as error:
            logging.error("Failed to connect to AWS Batch service.")

        return False, "AWS Batch service unavailable."

    def health_check_storage_service(self) -> Tuple[bool, str]:
        """Checks the health of the AWS storage service.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        try:
            resp = self.get_aws_client(ClientType.S3).list_buckets()
            valid_session = resp["ResponseMetadata"]["HTTPStatusCode"] == 200
            if valid_session:
                return True, "AWS S3 storage available."
        except ClientError as error:
            logging.error("Failed to connect to AWS S3.")

        return False, "AWS S3 storage unavailable."

    def health_check_secret_storage(self) -> Tuple[bool, str]:
        """Checks the health of the Azure key vault.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        try:
            resp = self.get_aws_client(ClientType.SSM).describe_sessions(State="Active")
            valid_session = resp["ResponseMetadata"]["HTTPStatusCode"] == 200
            if valid_session:
                return True, "AWS SSM available."
        except ClientError as error:
            logging.error(
                "Failed to validate connection to AWS parameter store."
            )
        return False, "AWS SSM unavailable."
