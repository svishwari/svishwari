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
from huxunify.api.route.utils import get_db_client
from huxunify.api import config, constants as api_const


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
            submit (bool): Submit job to AWS bool.
        Returns:

        """
        # Connect to AWS Batch
        if aws_batch_connector is None:
            aws_batch_connector = AWSBatchConnector(
                job_head_name,
                self.audience_delivery_job_id,
            )
        self.aws_batch_connector = aws_batch_connector

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
        if self.aws_batch_connector is None:
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
    destination_id,
    audience_id,
    audience_router_batch_size: int = 5000,
) -> DestinationBatchJob:
    """Get the configuration for the aws batch config of a destination.

    Args:
        database (MongoClient): The mongo database client.
        destination_id (ObjectId): The ID of the destination.
        audience_id (ObjectId): The ID of the audience.
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

    # Setup AWS Batch env vars and secrets
    aws_env_dict = {
        db_const.DELIVERY_JOB_ID.upper(): str(
            audience_delivery_job[db_const.ID]
        ),
        api_const.BATCH_SIZE.upper(): str(audience_router_batch_size),
        config.HOST: config.MONGO_DB_HOST,
        config.PORT: config.MONGO_DB_PORT,
        config.USER_NAME: config.MONGO_DB_USERNAME,
        config.SSL_CERT_PATH: config.MONGO_SSL_CERT,
        config.MONITORING_CONFIG_CONST: config.MONITORING_CONFIG,
    }

    aws_secret_dict = {
        config.PASSWORD: config.MONGO_DB_PASSWORD,
        **map_destination_credentials_to_dict(delivery_platform),
    }
    return DestinationBatchJob(
        database,
        audience_delivery_job[db_const.ID],
        aws_secret_dict,
        aws_env_dict,
    )


class Courier:
    """
    Courier that delivers audiences. Tips optional.
    """

    def __init__(
        self, engagement_id: ObjectId, db_client=get_db_client()
    ) -> None:
        """Init method for the courier object

        Args:
            engagement_id (ObjectId): The engagement ObjectId.
            db_client (MongoClient): Mongo database client.

        Returns:

        """
        self.db_client = db_client
        self.engagement_id = engagement_id

    def get_delivery_route(self, audience_ids: list = None) -> dict:
        """Set up the delivery route for an engagement's audiences.

        Args:
            audience_ids (list): List of audience IDs.

        Returns:
            dict: Returns the delivery route.
        """

        # use audiences unless passed in
        if not audience_ids:
            # TODO - set engagement object when engagements are in Database Library
            # simulate for now
            engagements = self.db_client[db_const.DATA_MANAGEMENT_DATABASE][
                "engagements"
            ]
            audience_ids = engagements.find_one(self.engagement_id)[
                db_const.AUDIENCES
            ]

        # TODO - add database function to simplify getting an audience.
        audiences = self.db_client[db_const.DATA_MANAGEMENT_DATABASE][
            db_const.AUDIENCES
        ]

        # prep all the audiences for delivery
        delivery_route = {}
        for audience_id in audience_ids:
            # get the audience object
            audience = audiences.find_one(audience_id)
            delivery_route[audience_id] = []

            # process each destination listed in the audience
            for destination_id in audience[db_const.DESTINATIONS]:
                delivery_route[audience_id].append(destination_id)

        return delivery_route


if __name__ == "__main__":
    pass
