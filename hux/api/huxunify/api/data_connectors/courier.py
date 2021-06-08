"""
purpose of this file is to house all delivery related components.
 - delivery of an audience
"""
from http import HTTPStatus
from bson import ObjectId
from pymongo import MongoClient
from huxunifylib.database import constants as db_const
from huxunifylib.database.delivery_platform_management import (
    set_delivery_job,
    get_delivery_platform,
    set_delivery_job_status,
)
from huxunifylib.connectors.aws_batch_connector import AWSBatchConnector
from huxunify.api import constants as api_const, config as cfg
from huxunify.api.config import get_config


def map_destination_credentials_to_dict(destination: dict) -> dict:
    """Map destination credentials to a dictionary for aws batch.
    Handle any custom logic here in the future for new destination types.

    Args:
        destination (dict): The destination object.

    Returns:
        dict: The credential dictionary.
    """
    cred_dict = {}

    # skip if no authentication details provided.
    if db_const.DELIVERY_PLATFORM_AUTH not in destination:
        return cred_dict

    # assign the auth credentials to the secrets dict
    for key, value in destination[db_const.DELIVERY_PLATFORM_AUTH].items():
        cred_dict[key] = value
    return cred_dict


class DestinationBatchJob:
    """
    Class for housing the Destination batch config.
    """

    def __init__(
        self,
        database: MongoClient,
        audience_delivery_job_id: ObjectId,
        aws_secrets: dict,
        aws_envs: dict,
    ) -> None:
        """Init the class with the config variables

        Args:
            database (MongoClient): The mongo database client.
            audience_delivery_job_id (ObjectId): ObjectId of the audience delivery job.
            aws_secrets (dict): The AWS secret dict for a batch job.
            aws_envs (dict): The AWS env dict for a batch job.

        Returns:

        """
        self.database = database
        self.audience_delivery_job_id = audience_delivery_job_id
        self.aws_secrets = aws_secrets
        self.aws_envs = aws_envs
        self.aws_batch_connector = None
        self.result = None

    def register(
        self,
        job_head_name: str = "audiencerouter",
        aws_batch_mem_limit: int = 2048,
        aws_batch_connector: AWSBatchConnector = None,
    ) -> None:
        """Register a destination job

        Args:
            job_head_name (str): The aws batch job head name.
            aws_batch_mem_limit (int): AWS Batch RAM limit.
            aws_batch_connector (AWSBatchConnector): AWS batch connector.

        Returns:

        """
        # Connect to AWS Batch
        if aws_batch_connector is None:
            aws_batch_connector = AWSBatchConnector(
                job_head_name,
                self.audience_delivery_job_id,
            )
        self.aws_batch_connector = aws_batch_connector

        # get the configuration values
        config = get_config()

        # Register AWS batch job
        response_batch_register = self.aws_batch_connector.register_job(
            job_role_arn=config.AUDIENCE_ROUTER_JOB_ROLE_ARN,
            exec_role_arn=config.AUDIENCE_ROUTER_EXECUTION_ROLE_ARN,
            exec_image=config.AUDIENCE_ROUTER_IMAGE,
            env_dict=self.aws_envs,
            secret_dict=self.aws_secrets,
            aws_batch_mem_limit=aws_batch_mem_limit,
        )

        if (
            response_batch_register["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.OK.value
        ):
            set_delivery_job_status(
                self.database,
                self.audience_delivery_job_id,
                db_const.STATUS_FAILED,
            )
            self.result = db_const.STATUS_FAILED
            return

        self.result = db_const.STATUS_PENDING

    def submit(self) -> None:
        """Submit a destination job

        Args:

        Returns:

        """
        # Connect to AWS Batch
        if (
            self.aws_batch_connector is None
            and self.aws_batch_connector.job_def_name is not None
            and not isinstance(self.aws_batch_connector, AWSBatchConnector)
        ):
            raise Exception("Must register a job first.")

        # Submit the AWS batch job
        response_batch_submit = self.aws_batch_connector.submit_job()

        status = db_const.STATUS_IN_PROGRESS
        if (
            response_batch_submit["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.OK.value
        ):
            status = db_const.STATUS_FAILED

        set_delivery_job_status(
            self.database,
            self.audience_delivery_job_id,
            status,
        )
        self.result = status


def get_destination_config(
    database: MongoClient,
    audience_id,
    destination_id,
    audience_router_batch_size: int = 5000,
) -> DestinationBatchJob:
    """Get the configuration for the aws batch config of a destination.

    Args:
        database (MongoClient): The mongo database client.
        audience_id (ObjectId): The ID of the audience.
        destination_id (ObjectId): The ID of the destination.
        audience_router_batch_size (int): Audience router AWS batch size.

    Returns:
        DestinationBatchJob: Destination batch job object.
    """
    audience_delivery_job = set_delivery_job(
        database, audience_id, destination_id, []
    )

    delivery_platform = get_delivery_platform(
        database,
        destination_id,
    )

    # get the configuration values
    config = get_config()

    # Setup AWS Batch env vars and secrets
    aws_env_dict = {
        db_const.DELIVERY_JOB_ID.upper(): str(
            audience_delivery_job[db_const.ID]
        ),
        api_const.BATCH_SIZE.upper(): str(audience_router_batch_size),
        cfg.HOST: config.MONGO_DB_HOST,
        cfg.PORT: str(config.MONGO_DB_PORT),
        cfg.USER_NAME: config.MONGO_DB_USERNAME,
        cfg.SSL_CERT_PATH: config.MONGO_SSL_CERT,
        config.MONITORING_CONFIG_CONST: config.MONITORING_CONFIG,
        api_const.AUDIENCE_ROUTER_STUB_TEST: "1",  # CDM STUB VALUE
    }

    aws_secret_dict = {
        cfg.PASSWORD: config.MONGO_DB_PASSWORD,
        **map_destination_credentials_to_dict(delivery_platform),
    }
    return DestinationBatchJob(
        database,
        audience_delivery_job[db_const.ID],
        aws_secret_dict,
        aws_env_dict,
    )


def get_audience_destination_pairs(engagement_audiences: dict):
    """

    Args:
        engagement:

    Returns:

    """
    return [
        [aud[db_const.ID], dest[db_const.DELIVERY_PLATFORM_ID]]
        for aud in engagement_audiences
        for dest in aud[db_const.DESTINATIONS]
    ]


if __name__ == "__main__":
    pass
