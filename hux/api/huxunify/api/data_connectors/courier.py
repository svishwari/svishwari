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
from huxunifylib.util.general.const import (
    MongoDBCredentials,
    FacebookCredentials,
)
from huxunifylib.util.audience_router.const import AudienceRouterConfig
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api import constants as api_const
from huxunify.api.config import get_config


def map_destination_credentials_to_dict(destination: dict) -> tuple:
    """Map destination credentials to a dictionary for aws batch.
    Handle any custom logic here in the future for new destination types.

    Args:
        destination (dict): The destination object.

    Returns:
        tuple: The credential tuple for (env, secrets).
    """

    # skip if no authentication details provided.
    if db_const.DELIVERY_PLATFORM_AUTH not in destination:
        raise KeyError(
            f"No authentication details for {destination[db_const.DELIVERY_PLATFORM_NAME]}"
        )

    # get auth
    auth = destination[db_const.DELIVERY_PLATFORM_AUTH]
    secret_dict = {}
    if (
        destination[db_const.DELIVERY_PLATFORM_NAME].upper()
        == db_const.DELIVERY_PLATFORM_FACEBOOK.upper()
    ):
        # TODO work with ORCH so we dont' have to send creds in env_dict
        env_dict = {
            FacebookCredentials.FACEBOOK_AD_ACCOUNT_ID.name: parameter_store.get_store_value(
                auth[api_const.FACEBOOK_AD_ACCOUNT_ID]
            ),
            FacebookCredentials.FACEBOOK_APP_ID.name: parameter_store.get_store_value(
                auth[api_const.FACEBOOK_APP_ID]
            ),
            FacebookCredentials.FACEBOOK_ACCESS_TOKEN.name: parameter_store.get_store_value(
                auth[api_const.FACEBOOK_ACCESS_TOKEN]
            ),
            FacebookCredentials.FACEBOOK_APP_SECRET.name: parameter_store.get_store_value(
                auth[api_const.FACEBOOK_APP_SECRET]
            ),
        }
    else:
        raise KeyError(
            f"No configuration for {destination[db_const.DELIVERY_PLATFORM_NAME]}"
        )

    return env_dict, secret_dict


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

    # get destination specific env values
    ds_env_dict, ds_secret_dict = map_destination_credentials_to_dict(
        delivery_platform
    )

    # Setup AWS Batch env dict
    env_dict = {
        AudienceRouterConfig.DELIVERY_JOB_ID.name: str(
            audience_delivery_job[db_const.ID]
        ),
        AudienceRouterConfig.BATCH_SIZE.name: str(audience_router_batch_size),
        MongoDBCredentials.MONGO_DB_HOST.name: config.MONGO_DB_HOST,
        MongoDBCredentials.MONGO_DB_PORT.name: str(config.MONGO_DB_PORT),
        MongoDBCredentials.MONGO_DB_USERNAME.name: config.MONGO_DB_USERNAME,
        MongoDBCredentials.MONGO_SSL_CERT.name: api_const.AUDIENCE_ROUTER_CERT_PATH,
        api_const.AUDIENCE_ROUTER_STUB_TEST: api_const.AUDIENCE_ROUTER_STUB_VALUE,
        **ds_env_dict,
    }

    # setup the secrets dict
    secret_dict = {
        MongoDBCredentials.MONGO_DB_PASSWORD.name: api_const.AUDIENCE_ROUTER_MONGO_PASSWORD_FROM,
        **ds_secret_dict,
    }

    return DestinationBatchJob(
        database,
        audience_delivery_job[db_const.ID],
        secret_dict,
        env_dict,
    )


def get_audience_destination_pairs(audiences: list) -> list:
    """function to get all the audience destination pairs for a list
    of audiences within an engagement.

    Args:
        audiences (list): list of audiences

    Returns:
        list: list of tuples [(audience_id, destination_id),..]
    """

    if not audiences or not any(x for x in audiences if x):
        raise TypeError("Empty list provided.")

    # validate to ensure list of dicts has destinations
    if any(x for x in audiences if db_const.DESTINATIONS not in x):
        raise TypeError("must be a list of destinations.")

    return [
        [aud[db_const.OBJECT_ID], dest[db_const.OBJECT_ID]]
        for aud in audiences
        for dest in aud[db_const.DESTINATIONS]
    ]


if __name__ == "__main__":
    pass
