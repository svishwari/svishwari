"""Utility module for the cloud connector objects"""
from huxunify.api.data_connectors.cloud_connectors.cloud_client import (
    CloudClient,
)
from huxunify.api.data_connectors.cloud_connectors.azure_client import (
    AzureClient,
)
from huxunify.api.config import get_config
from huxunify.api.data_connectors.cloud_connectors.aws_client import AWSClient


# pylint: disable=no-else-return
def get_cloud_client(config=get_config()) -> CloudClient:
    """Gets the proper cloud client

    Args:
        config (config): config object.

    Returns:
        CloudClient: a child class of the CloudClient class

    Raises:
        Exception: Raised if an unsupported exception is raised.
    """

    if config.CLOUD_PROVIDER.lower() == "aws":
        return AWSClient()

    elif config.CLOUD_PROVIDER.lower() == "azure":
        return AzureClient()

    raise Exception(
        f"Cloud provider {config.CLOUD_PROVIDER} is not supported!"
    )
