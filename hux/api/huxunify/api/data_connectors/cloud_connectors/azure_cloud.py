"""Module for Azure cloud operations"""
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from huxunify.api.data_connectors.cloud_connectors.cloud import Cloud

# pylint: disable=missing-raises-doc
class Azure(Cloud):
    """Class for Azure cloud operations"""

    provider = "AZURE"

    def get_secret(self, secret_name: str, **kwargs) -> str:
        """Retrieve secret from cloud.

        Args:
            secret_name (str): Name of the secret.
            kwargs (dict): extra parameters.

        Returns:
            str: The value of the secret.
        """
        try:
            vault_uri = (
                f"https://{self.config.AZURE_KEY_VAULT_NAME}.vault.azure.net"
            )
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_uri, credential=credential)
            return client.get_secret(secret_name).value
        except Exception as exc:
            raise exc

    def set_secret(self, secret_name: str, value: str, **kwargs) -> None:
        """Set the secret in the cloud.

        Args:
            secret_name (str): Name of the secret.
            value (str): The value of the secret.
            kwargs (dict): extra parameters.

        Returns:
            None
        """
        try:
            vault_uri = (
                f"https://{self.config.AZURE_KEY_VAULT_NAME}.vault.azure.net"
            )
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_uri, credential=credential)
            client.set_secret(name=secret_name, value=value)
        except Exception as exc:
            raise exc

    def upload_file(
        self, file_name: str, file_type: str, user_name: str, **kwargs
    ) -> bool:
        """Uploads a file to Azure Blob

        Args:
            file_name (str): name of the file to upload.
            file_type (str): type of the file to upload.
            user_name (str): name of the user uploading the file.
            kwargs (dict): extra parameters.

        Returns:
            bool: bool indicator if the upload was successful

        """
        raise NotImplementedError()

    def download_file(self, file_name: str, user_name: str, **kwargs) -> bool:
        """Download a file from the cloud.

        Args:
            file_name (str): Name of the file to upload.
            user_name (str): Name of the user uploading the file.
            kwargs (dict): extra parameters.

        Returns:

        """
        raise NotImplementedError()

    def health_check_batch_service(self) -> dict:
        """Checks the health of the cloud batch service.

        Returns:
            dict: Health details of the batch service.
        """
        raise NotImplementedError()

    def health_check_storage_service(self) -> dict:
        """Checks the health of the cloud storage service.

        Returns:
            dict: Health details of the storage service.
        """
        raise NotImplementedError()


if __name__ == "__main__":
    pass
