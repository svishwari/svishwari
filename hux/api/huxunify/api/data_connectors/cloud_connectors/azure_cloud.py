"""Module for Azure cloud operations"""
import logging
from typing import Tuple

from azure.batch import BatchServiceClient
from azure.batch.batch_auth import SharedKeyCredentials
from azure.batch.models import BatchErrorException
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient

from huxunify.api.data_connectors.cloud_connectors.cloud import Cloud
import huxunify.api.constants as api_c

# pylint: disable=missing-raises-doc
from huxunify.api.prometheus import record_health_status_metric


class Azure(Cloud):
    """Class for Azure cloud operations"""

    provider = "AZURE"

    def __init__(self):
        """Initialize Azure Cloud object

        Args:
        """
        self.vault_url = (
            f"https://{self.config.AZURE_KEY_VAULT_NAME}.vault.azure.net"
        )

    def get_secret(self, secret_name: str, **kwargs) -> str:
        """Retrieve secret from cloud.

        Args:
            secret_name (str): Name of the secret.
            **kwargs (dict): extra parameters.

        Returns:
            str: The value of the secret.
        """
        try:
            credential = DefaultAzureCredential()
            client = SecretClient(
                vault_url=self.vault_url, credential=credential
            )
            return client.get_secret(secret_name).value
        except Exception as exc:
            logging.error(
                "Failed to get %s from Azure key vault.", secret_name
            )
            raise exc

    def set_secret(self, secret_name: str, value: str, **kwargs) -> None:
        """Set the secret in the cloud.

        Args:
            secret_name (str): Name of the secret.
            value (str): The value of the secret.
            **kwargs (dict): function keyword arguments.

        Returns:
        """
        try:
            credential = DefaultAzureCredential()
            client = SecretClient(
                vault_url=self.vault_url, credential=credential
            )
            client.set_secret(name=secret_name, value=value)
        except Exception as exc:
            logging.error("Failed to set %s in Azure key vault.", secret_name)
            raise exc

    def upload_file(
        self, file_name: str, file_type: str, user_name: str, **kwargs
    ) -> bool:
        """Uploads a file to Azure Blob

        Args:
            file_name (str): name of the file to upload.
            file_type (str): type of the file to upload.
            user_name (str): name of the user uploading the file.
            **kwargs (dict): function keyword arguments.

        Returns:
            bool: bool indicator if the upload was successful

        """
        raise NotImplementedError()

    def download_file(self, file_name: str, user_name: str, **kwargs) -> bool:
        """Download a file from the cloud.

        Args:
            file_name (str): Name of the file to upload.
            user_name (str): Name of the user uploading the file.
            **kwargs (dict): function keyword arguments.

        Returns:
            bool: indication that download was successful.
        """
        raise NotImplementedError()

    def health_check_batch_service(self) -> Tuple[bool, str]:
        """Checks the health of the cloud batch service.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """

        credentials = SharedKeyCredentials(
            self.config.AZURE_BATCH_ACCOUNT_NAME,
            self.config.AZURE_BATCH_ACCOUNT_KEY,
        )
        batch_client = BatchServiceClient(
            credentials, self.config.AZURE_BATCH_ACCOUNT_URL
        )
        status = True, f"Azure batch service available."

        try:
            batch_client.account.list_supported_images()
        except BatchErrorException as exc:
            status = False, getattr(exc, "message", repr(exc))

        record_health_status_metric(
            api_c.AZURE_BATCH_CONNECTION_HEALTH, status[0]
        )
        return status

    def health_check_storage_service(self) -> Tuple[bool, str]:
        """Checks the health of the cloud storage service.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """

        connection_url = (
            f"https:AccountName={self.config.AZURE_STORAGE_ACCOUNT_NAME}"
            f";AccountKey={self.config.AZURE_STORAGE_ACCOUNT_KEY}"
        )

        c = BlobClient(
            account_url=connection_url,
            container_name=self.config.AZURE_STORAGE_CONTAINER_NAME,
            blob_name=self.config.AZURE_STORAGE_BLOB_NAME,
        )
        client_status = c.exists()

        status = (
            client_status,
            f"Azure Blob service available."
            if client_status
            else f"Azure Blob service unavailable.",
        )

        record_health_status_metric(
            api_c.AZURE_BLOB_CONNECTION_HEALTH, status[0]
        )
        return status


if __name__ == "__main__":
    pass
