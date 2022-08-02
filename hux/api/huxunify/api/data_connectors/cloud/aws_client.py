"""Module for AWS cloud operations"""
import logging
from pathlib import PurePath
from typing import Tuple
from enum import Enum

import boto3
from botocore.exceptions import ClientError

from huxunify.api.data_connectors.cloud.cloud_client import (
    CloudClient,
)
from huxunify.api.config import get_config, Config
import huxunify.api.constants as api_c
from huxunify.api.prometheus import record_health_status, Connections


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
        self, client_type: ClientType, region_name: str = None
    ) -> boto3.client:
        """Retrieves AWS client.
        (Most of them)

        Args:
            client_type (ClientType): client type.
            region_name (str): name of the AWS region.

        Returns:
            Response: boto3 client

        """
        return boto3.client(
            client_type.value,
            region_name=region_name if region_name else self.config.AWS_REGION,
        )

    def get_secret(self, secret_name: str, **kwargs) -> str:
        """Retrieve secret from AWS Parameter Store.

        Args:
            secret_name (str): Name of the secret.
            **kwargs (dict): function keyword arguments.

        Returns:
            str: The value of the secret.

        Raises:
            ClientError: Error if the operation fails in AWS.
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

        Raises:
            ClientError: Error if the operation fails in AWS.
        """
        try:
            self.get_aws_client(ClientType.SSM).put_parameter(
                Name=secret_name,
                Value=value,
                Type="SecureString",
                Overwrite=True,
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
            bool: indication that upload was successful.
        """
        bucket = self.config.S3_DATASET_BUCKET
        object_name = PurePath(file_name).name

        # If S3 object_name was not specified, use file_name

        extraargs = {
            "Metadata": {
                api_c.CREATED_BY: user_name if user_name else "",
                api_c.TYPE: file_type if file_type else "",
            }
        }
        logging.info("Uploading %s file to AWS bucket %s", file_name, bucket)
        try:
            # Upload the file
            s3_client = self.get_aws_client(ClientType.S3)
            _ = s3_client.upload_file(
                file_name, bucket, object_name, extraargs
            )

        except ClientError as exception:
            logging.error(
                "Failed to upload file %s to %s : %s",
                file_name,
                bucket,
                exception,
            )
            return False
        logging.info("Uploaded %s file to %s", file_name, bucket)
        return True

    def download_file(self, file_name: str, user_name: str, **kwargs) -> bool:
        """Download a file from AWS S3.

        Args:
            file_name (str): Name of the file to upload.
            user_name (str): Name of the user uploading the file.
            **kwargs (dict): function keyword arguments.

        Returns:
            bool: indication that download was successful.
        """
        bucket = self.config.S3_DATASET_BUCKET

        logging.info("Downloading %s file from %s", file_name, bucket)
        try:
            s3_client = self.get_aws_client(ClientType.S3)
            with open(file_name, "wb") as output_file:
                s3_client.download_fileobj(bucket, file_name, output_file)
        except ClientError as exception:
            logging.error(
                "Failed to download file object %s from %s : %s",
                file_name,
                bucket,
                exception,
            )
            return False
        logging.info("Downloaded %s file from %s", file_name, bucket)
        return True

    def __check_aws_health_connection(
        self, client: ClientType, client_method: str, method_args: dict
    ) -> Tuple[bool, str]:
        """Validate an AWS service connection.

        Args:
            client (ClientType): type of AWS client to use.
            client_method (str): name of the method to call.
            method_args (dict): arguments for the method.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        try:
            # lookup the health test to run from api constants
            resp = getattr(self.get_aws_client(client), client_method)(
                **method_args
            )
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True, f"{client.value} available."
            return (
                False,
                f"{client.value} unavailable. Received status code: "
                f"{resp['ResponseMetadata']['HTTPStatusCode']}",
            )
        except Exception as exception:  # pylint: disable=broad-except
            # report the generic error message
            return (
                False,
                f"{client.value} unavailable. An error occured: "
                f"{getattr(exception, 'message', repr(exception))}",
            )

    @record_health_status(Connections.STORAGE_SERVICE)
    def health_check_storage_service(self) -> Tuple[bool, str]:
        """Checks the health of the AWS storage service.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        return self.__check_aws_health_connection(
            client=ClientType.S3,
            client_method="get_bucket_location",
            method_args={api_c.AWS_BUCKET: self.config.S3_DATASET_BUCKET},
        )

    @record_health_status(Connections.SECRET_STORAGE_SERVICE)
    def health_check_secret_storage(self) -> Tuple[bool, str]:
        """Checks the health of the Azure key vault.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        return self.__check_aws_health_connection(
            client=ClientType.SSM,
            client_method="get_parameter",
            method_args={"Name": "unifieddb_host_alias"},
        )
