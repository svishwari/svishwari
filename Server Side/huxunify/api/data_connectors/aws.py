"""
purpose of this file is for interacting with aws
"""
from os import getenv
import boto3


# get aws connection params
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = getenv("AWS_REGION")


def get_aws_client(
    client="s3",
    aws_access_key=AWS_ACCESS_KEY_ID,
    aws_secret_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
):
    """
    quick and dirty function for getting most AWS clients
    :param client:
    :param resource:
    :param aws_access_key:
    :param aws_secret_key:
    :param region_name:
    :return: aws client
    """
    return boto3.client(
        client,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name,
    )
