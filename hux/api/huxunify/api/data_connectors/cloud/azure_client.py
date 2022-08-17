"""Module for Azure cloud operations."""
import logging
from typing import Tuple
from pathlib import Path

from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import ContainerClient

from huxunify.api.data_connectors.cloud.cloud_client import (
    CloudClient,
)
from huxunify.api.config import get_config, Config
from huxunify.api.prometheus import record_health_status, Connections
from huxunify.api import constants as api_c


class AzureClient(CloudClient):
    """Class for Azure cloud operations."""

    provider = "azure"

    def __init__(self, config: Config = get_config()):
        """Instantiate the Azure client class."""

        super().__init__(config)

        self.vault_url = (
            f"https://{self.config.AZURE_KEY_VAULT_NAME}.vault.azure.net"
        )
        self.storage_container_name = self.config.AZURE_STORAGE_CONTAINER_NAME
        self.storage_connection_string = (
            self.config.AZURE_STORAGE_CONNECTION_STRING
        )

    def get_secret_client(self) -> SecretClient:
        """Get Azure Secret client.

        Returns:
            SecretClient: Azure secret client.

        Raises:
            Exception: Exception that will be raised if the operation fails.
        """

        try:
            return SecretClient(
                vault_url=self.vault_url,
                credential=ManagedIdentityCredential(
                    client_id=self.config.AZURE_MANAGED_IDENTITY_CLIENT_ID,
                    identity_config={
                        api_c.AZURE_OBJECT_ID: self.config.AZURE_MANAGED_IDENTITY_OBJECT_ID
                    },
                ),
            )
        except Exception as exc:
            logging.error("Failed to initialise Azure secret client.")
            raise exc

    def get_secret(self, secret_name: str, **kwargs) -> str:
        """Retrieve secret from cloud.

        Args:
            secret_name (str): Name of the secret.
            **kwargs (dict): extra parameters.

        Returns:
            str: The value of the secret.

        Raises:
            Exception: Exception that will be raised if the operation fails.
        """

        try:
            # gets the latest version of the secret if no version parameter is
            # mentioned
            return self.get_secret_client().get_secret(secret_name).value
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

        Raises:
            Exception: Exception that will be raised if the operation fails.
        """

        try:
            # creates a new secret if a secret with this secret name doesn't
            # exist already, sets a new latest version of secret otherwise
            self.get_secret_client().set_secret(name=secret_name, value=value)
        except Exception as exc:
            logging.error("Failed to set %s in Azure key vault.", secret_name)
            raise exc

    # pylint:disable=broad-except
    def upload_file(
        self, file_name: str, file_type: str, user_name: str, **kwargs
    ) -> bool:
        """Uploads a file to Azure Blob.

        Args:
            file_name (str): name of the file to upload.
            file_type (str): type of the file to upload.
            user_name (str): name of the user uploading the file.
            **kwargs (dict): function keyword arguments.

        Returns:
            bool: bool indicator if the upload was successful.
        """

        container_name = self.config.AZURE_STORAGE_CONTAINER_NAME
        connection_string = self.config.AZURE_STORAGE_CONNECTION_STRING

        try:
            logging.info(
                "Uploading %s to Azure blob container: %s",
                file_name,
                container_name,
            )
            container_client = ContainerClient.from_connection_string(
                connection_string, container_name
            )
            blob_client = container_client.get_blob_client(
                Path(file_name).name
            )

            metadata = {
                api_c.CREATED_BY: user_name if user_name else "",
                api_c.TYPE: file_type if file_type else "",
            }
            with open(Path(file_name).name, "rb") as data:
                blob_client.upload_blob(data=data, metadata=metadata)
                logging.info(
                    "Finished uploading %s to Azure blob container: %s",
                    file_name,
                    container_name,
                )
        except Exception as exc:
            logging.error(
                "Failed to upload %s to blob container: %s",
                file_name,
                container_name,
            )
            logging.error(exc)
            return False

        return True

    # pylint:disable=broad-except
    def download_file(self, file_name: str, user_name: str, **kwargs) -> bool:
        """Download a file from the cloud.

        Args:
            file_name (str): Name of the file to upload.
            user_name (str): Name of the user uploading the file.
            **kwargs (dict): function keyword arguments.

        Returns:
            bool: indication that download was successful.

        Raises:
            NotImplementedError: Error if function is not implemented.
        """

        container_name = self.config.AZURE_STORAGE_CONTAINER_NAME
        connection_string = self.config.AZURE_STORAGE_CONNECTION_STRING

        try:
            logging.info(
                "Downloading %s from Azure blob container: %s",
                file_name,
                container_name,
            )
            container_client = ContainerClient.from_connection_string(
                connection_string, container_name
            )
            blob_client = container_client.get_blob_client(
                Path(file_name).name
            )

            with open(file_name, "wb") as file_writer:
                download_stream = blob_client.download_blob()
                file_writer.write(download_stream.readall())
                logging.info(
                    "Finished downloading %s from Azure blob container: %s",
                    file_name,
                    container_name,
                )
        except Exception as exc:
            logging.error(
                "Failed to download %s from blob container: %s",
                file_name,
                container_name,
            )
            logging.error(exc)
            return False

        return True

    @record_health_status(Connections.STORAGE_SERVICE)
    def health_check_storage_service(self) -> Tuple[bool, str]:
        """Checks the health of the azure blob storage.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message.
        """

        container_client = ContainerClient.from_connection_string(
            self.storage_connection_string, self.storage_container_name
        )
        client_status = container_client.exists()

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
            Tuple[bool, str]: Returns bool for health status and message.
        """

        secret_name = "unifieddb-rw"

        try:
            self.get_secret(secret_name)
            return True, "Azure key vault available."
        except Exception as exc:
            logging.error(
                "Failed to get %s from Azure key vault. "
                "Azure key vault is unavailable",
                secret_name,
            )
            logging.error(exc)
            return False, "Azure key vault unavailable."
