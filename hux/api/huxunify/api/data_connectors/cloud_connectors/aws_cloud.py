"""Module for AWS cloud operations"""
import logging

import boto3
import botocore

from huxunify.api.data_connectors.cloud_connectors.cloud import Cloud
import huxunify.api.constants as api_c

# pylint: disable=missing-raises-doc
class AWS(Cloud):
    """Class for AWS cloud operations"""

    provider = "AWS"

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

    def health_check_batch_service(self) -> dict:
        """Checks the health of the AWS batch service.

        Returns:
            dict: Health details of the batch service.
        """
        raise NotImplementedError()

    def health_check_storage_service(self) -> dict:
        """Checks the health of the AWS storage service.

        Returns:
            dict: Health details of the storage service.
        """
        raise NotImplementedError()