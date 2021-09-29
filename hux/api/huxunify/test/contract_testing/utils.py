"""
Utils for contract testing
"""
from huxunifylib.util.general.logging import logger


def upload_pact_files_to_s3(folder: str) -> None:
    """Uploads pacts to required s3 buckets.
     Args:
        folder (str) : Path to folder where pact files are located.

    Returns:
        None
    """
    logger.info("Uploading pacts from %s to S3", folder)
    # TODO Upload contracts to S3
