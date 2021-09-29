"""
Utils for contract testing
"""
from huxunifylib.util.general.logging import logger


def upload_pact_files_to_s3(folder: str):
    logger.info(f"Uploading pacts from {folder} to S3")
    # TODO Upload contracts to S3
