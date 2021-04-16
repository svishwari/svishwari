"""
purpose of this file is for interacting with aws
"""
from os import getenv
from typing import Any

import boto3

# get aws connection params
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = getenv("AWS_REGION")


def get_aws_client(
    client: str = "s3",
    aws_access_key: str = AWS_ACCESS_KEY_ID,
    aws_secret_key: str = AWS_SECRET_ACCESS_KEY,
    region_name: str = AWS_REGION,
) -> Any:
    """ quick and dirty function for getting most AWS clients

    Args:
        client (str): client string
        aws_access_key (str): AWS access key
        aws_secret_key (str): AWS secret key
        region_name (str): Region Name

    Returns:
        Response: decorator

    """
    return boto3.client(
        client,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name,
    )
