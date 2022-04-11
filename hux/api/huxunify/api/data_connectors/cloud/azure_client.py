"""Module for Azure cloud operations"""
import logging
from typing import Tuple

from azure.batch import BatchServiceClient
from azure.batch.batch_auth import SharedKeyCredentials
from azure.batch.models import BatchErrorException
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient

from huxunify.api.data_connectors.cloud.cloud_client import (
    CloudClient,
)
from huxunify.api.config import get_config, Config
from huxunify.api.prometheus import record_health_status, Connections


class AzureClient(CloudClient):
    """Class for Azure cloud operations"""

    provider = "azure"

    def __init__(self, config: Config = get_config()):
        """Instantiate the Azure client class"""
        super().__init__(config)
        self.vault_url = (
            f"https://{self.config.AZURE_KEY_VAULT_NAME}.vault.azure.net"
        )
        self.blob_connection_url = (
            f"https:AccountName={self.config.AZURE_STORAGE_ACCOUNT_NAME}"
            f";AccountKey={self.config.AZURE_STORAGE_ACCOUNT_KEY}"
        )

    def get_secret(self, secret_name: str, **kwargs) -> str:
        """Retrieve secret from cloud.

        Args:
            secret_name (str): Name of the secret.
            **kwargs (dict): extra parameters.

        Returns:
            str: The value of the secret.

        Raises:
            Exception: Exception that will be raised if the operation fails
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

        Raises:
            Exception: Exception that will be raised if the operation fails
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
        container_name = self.config.AZURE_STORAGE_CONTAINER_NAME
        blob_name = self.config.AZURE_STORAGE_BLOB_NAME

        try:
            logging.info(
                "Uploading %s to Azure blob container: %s",
                file_name,
                container_name,
            )
            client = BlobClient.from_connection_string(
                conn_str=self.blob_connection_url,
                container_name=container_name,
                blob_name=blob_name,
            )

            metadata = {
                api_c.CREATED_BY: user_name if user_name else "",
                api_c.TYPE: file_type if file_type else "",
            }
            with open(file_name, "rb") as data:
                client.upload_blob(data=data, metadata=metadata)
        except Exception as exc:
            logging.error("Failed to upload %s to blob container.", file_name)
            logging.error(exc)
            return False

        return True

    def download_file(self, file_name: str, user_name: str, **kwargs) -> bool:
        """Download a file from the cloud.

        Args:
            file_name (str): Name of the file to upload.
            user_name (str): Name of the user uploading the file.
            **kwargs (dict): function keyword arguments.

        Returns:
            bool: indication that download was successful.

        Raises:
            NotImplementedError: Error if function is not implemented
        """
        container_name = self.config.AZURE_STORAGE_CONTAINER_NAME
        blob_name = self.config.AZURE_STORAGE_BLOB_NAME

        try:
            logging.info(
                "Downloading %s from Azure blob container: %s",
                file_name,
                container_name,
            )
            client = BlobClient.from_connection_string(
                conn_str=self.blob_connection_url,
                container_name=container_name,
                blob_name=blob_name,
            )

            with open(file_name, "rb") as data:
                client.upload_blob(data=data, metadata=metadata)
        except Exception as exc:
            logging.error("Failed to upload %s to blob container.", file_name)
            logging.error(exc)
            return False

        return True

    @record_health_status(Connections.BATCH_SERVICE)
    def health_check_batch_service(self) -> Tuple[bool, str]:
        """Checks the health of the Azure batch service.

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
        status = True, "Azure batch service available."

        try:
            batch_client.account.list_supported_images()
        except BatchErrorException as exc:
            status = False, getattr(exc, "message", repr(exc))

        return status

    @record_health_status(Connections.STORAGE_SERVICE)
    def health_check_storage_service(self) -> Tuple[bool, str]:
        """Checks the health of the azure blob storage.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """

        blob_client = BlobClient(
            account_url=self.blob_connection_url,
            container_name=self.config.AZURE_STORAGE_CONTAINER_NAME,
            blob_name=self.config.AZURE_STORAGE_BLOB_NAME,
        )
        client_status = blob_client.exists()

        status = (
            client_status,
            "Azure Blob service available."
            if client_status
            else "Azure Blob service unavailable.",
        )

        return status

    # pylint: disable=broad-except
    @record_health_status(Connections.SECRET_STORAGE_SERVICE)
    def health_check_secret_storage(self) -> Tuple[bool, str]:
        """Checks the health of the Azure key vault.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        secret_name = "<secret name here>"

        try:
            credential = DefaultAzureCredential()
            client = SecretClient(
                vault_url=self.vault_url, credential=credential
            )
            client.get_secret(secret_name)
            return True, "Azure key vault available."
        except Exception as exc:
            logging.error(
                "Failed to get %s from Azure key vault. Azure key vault is unavailable",
                secret_name,
            )
            logging.error(exc)
            return False, "Azure key vault unavailable."
