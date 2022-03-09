""" Module for base class for cloud operations"""
from typing import Tuple, TypeVar

from huxunify.api.config import get_config, Config


class CloudClient:
    """Base class for cloud operations"""

    def __new__(
        cls, config: Config = get_config()
    ) -> TypeVar("T", bound="CloudClient"):
        """override the new class to handle subclass mapping.

        Args:
            config (Config): configuration object.

        Returns:
            CloudClient: subclass of CloudClient.
        """
        provider = config.CLOUD_PROVIDER.lower()
        subclass_map = {
            subclass.provider.lower(): subclass
            for subclass in cls.__subclasses__()
        }
        subclass = (
            subclass_map[provider] if provider in subclass_map else CloudClient
        )
        return super(CloudClient, subclass).__new__(subclass)

    def __init__(self, config=get_config()):
        """Instantiate the cloud client base class

        Args:
            config (config): config object.
        """
        self.config = config

    def get_secret(self, secret_name: str, **kwargs) -> str:
        """Retrieve secret from cloud.

        Args:
            secret_name (str): Name of the secret.
            **kwargs (dict): function keyword arguments.

        Returns:
            str: The value of the secret.
        """
        raise NotImplementedError()

    def set_secret(self, secret_name: str, value: str, **kwargs) -> None:
        """Set the secret in the cloud.

        Args:
            secret_name (str): Name of the secret.
            value (str): The value of the secret.
            **kwargs (dict): function keyword arguments.

        Returns:
            None
        """

        raise NotImplementedError()

    def upload_file(
        self, file_name: str, file_type: str, user_name: str, **kwargs
    ) -> bool:
        """Upload a file to the cloud.

        Args:
            file_name (str): Name of the file to upload.
            file_type (str): Type of the file to upload.
            user_name (str): Name of the user uploading the file.
            **kwargs (dict): function keyword arguments.

        Returns:

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
        raise NotImplementedError()

    def health_check_storage_service(self) -> Tuple[bool, str]:
        """Checks the health of the cloud storage service.

        Returns:
            Tuple[bool, str]: Returns bool for health status and message
        """
        raise NotImplementedError()
