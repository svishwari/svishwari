""" Module for base class for cloud operations"""
from huxunify.api.config import Config, get_config

# pylint: disable=missing-raises-doc
class Cloud:
    """Base class for cloud operations"""

    provider = None
    config = None

    # pylint: disable=unused-argument, keyword-arg-before-vararg
    def __new__(cls, config: Config = get_config(), *args, **kwargs):
        cls.config = config
        subclass = next(
            filter(
                lambda clazz: clazz.provider.lower()
                == config.CLOUD_PROVIDER.lower(),
                cls.__subclasses__(),
            )
        )

        return object.__new__(subclass)

    def get_secret(self, secret_name: str, **kwargs) -> str:
        """Retrieve secret from cloud.

        Args:
            secret_name (str): Name of the secret.
            kwargs (dict): extra parameters.

        Returns:
            str: The value of the secret.
        """
        raise NotImplementedError()

    def set_secret(self, secret_name: str, value: str, **kwargs) -> None:
        """Set the secret in the cloud.

        Args:
            secret_name (str): Name of the secret.
            value (str): The value of the secret.
            kwargs (dict): extra parameters.

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
            kwargs (dict): extra parameters.

        Returns:

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
