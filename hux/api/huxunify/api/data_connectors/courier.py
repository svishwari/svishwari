"""
purpose of this file is to house all delivery related components.
 - delivery of an audience
"""
import logging
from http import HTTPStatus
from bson import ObjectId
from pymongo import MongoClient
from huxunifylib.database import constants as db_const
from huxunifylib.database.delivery_platform_management import (
    set_delivery_job,
    get_delivery_platform,
    set_delivery_job_status,
)
from huxunifylib.database.engagement_management import add_delivery_job
from huxunifylib.connectors import AWSBatchConnector
from huxunifylib.util.general.const import (
    MongoDBCredentials,
    FacebookCredentials,
    SFMCCredentials,
    TwilioCredentials,
)
from huxunifylib.util.audience_router.const import AudienceRouterConfig
from huxunify.api import constants as api_const
from huxunify.api.config import get_config
from huxunify.api.data_connectors.aws import (
    set_cloud_watch_rule,
    put_rule_targets_aws_batch,
)


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

    if (
        destination[db_const.DELIVERY_PLATFORM_TYPE]
        == db_const.DELIVERY_PLATFORM_FACEBOOK
    ):
        env_dict = {
            FacebookCredentials.FACEBOOK_AD_ACCOUNT_ID.name: auth[
                api_const.FACEBOOK_AD_ACCOUNT_ID
            ],
            FacebookCredentials.FACEBOOK_APP_ID.name: auth[
                api_const.FACEBOOK_APP_ID
            ],
        }
        secret_dict = {
            FacebookCredentials.FACEBOOK_ACCESS_TOKEN.name: auth[
                api_const.FACEBOOK_ACCESS_TOKEN
            ],
            FacebookCredentials.FACEBOOK_APP_SECRET.name: auth[
                api_const.FACEBOOK_APP_SECRET
            ],
        }

    elif (
        destination[db_const.DELIVERY_PLATFORM_TYPE]
        == db_const.DELIVERY_PLATFORM_SFMC
    ):
        env_dict = {
            SFMCCredentials.SFMC_CLIENT_ID.name: auth[
                api_const.SFMC_CLIENT_ID
            ],
            SFMCCredentials.SFMC_AUTH_URL.name: auth[
                api_const.SFMC_AUTH_BASE_URI
            ],
            SFMCCredentials.SFMC_ACCOUNT_ID.name: auth[
                api_const.SFMC_ACCOUNT_ID
            ],
            SFMCCredentials.SFMC_SOAP_ENDPOINT.name: auth[
                api_const.SFMC_SOAP_BASE_URI
            ],
            SFMCCredentials.SFMC_URL.name: auth[api_const.SFMC_REST_BASE_URI],
        }

        secret_dict = {
            SFMCCredentials.SFMC_CLIENT_SECRET.name: auth[
                api_const.SFMC_CLIENT_SECRET
            ]
        }
    elif (
        destination[db_const.DELIVERY_PLATFORM_TYPE]
        == db_const.DELIVERY_PLATFORM_TWILIO
    ):
        env_dict = {}
        secret_dict = {
            TwilioCredentials.TWILIO_AUTH_TOKEN.name: auth[
                api_const.TWILIO_AUTH_TOKEN
            ]
        }
    else:
        raise KeyError(
            f"No configuration for destination type: {destination[db_const.DELIVERY_PLATFORM_TYPE]}"
        )

    return env_dict, secret_dict


# pylint: disable=too-many-instance-attributes
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
        destination_type: str,
    ) -> None:
        """Init the class with the config variables

        Args:
            database (MongoClient): The mongo database client.
            audience_delivery_job_id (ObjectId): ObjectId of the audience delivery job.
            aws_secrets (dict): The AWS secret dict for a batch job.
            aws_envs (dict): The AWS env dict for a batch job.
            destination_type (str): The type of destination (i.e. facebook, sfcm)

        Returns:

        """
        self.database = database
        self.audience_delivery_job_id = audience_delivery_job_id
        self.aws_secrets = aws_secrets
        self.aws_envs = aws_envs
        self.destination_type = destination_type
        self.aws_batch_connector = None
        self.result = None
        self.scheduled = False

    def register(
        self,
        engagement_doc: dict,
        job_head_name: str = "audiencerouter",
        aws_batch_mem_limit: int = 2048,
        aws_batch_connector: AWSBatchConnector = None,
    ) -> None:
        """Register a destination job

        Args:
            engagement_doc (dict): Engagement document.
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
                db_const.AUDIENCE_STATUS_ERROR,
            )
            self.result = db_const.AUDIENCE_STATUS_ERROR
            return

        self.result = db_const.AUDIENCE_STATUS_DELIVERING

        # check if engagement has a delivery flight schedule set
        if not (
            engagement_doc and engagement_doc.get(api_const.DELIVERY_SCHEDULE)
        ):
            logging.warning(
                "Delivery schedule is not set for %s",
                engagement_doc[db_const.ID],
            )
            return

        # create the rule name
        cw_name = f"{engagement_doc[db_const.ID]}-{self.destination_type}"

        # TODO hookup converted cron job expression HUS-794
        if not set_cloud_watch_rule(
            cw_name,
            "cron(15 0 * * ? *)",
            config.AUDIENCE_ROUTER_JOB_ROLE_ARN,
        ):
            logging.error(
                "Error creating cloud watch rule for engagement with ID %s",
                engagement_doc[db_const.ID],
            )
            return

        # setup the batch params for the registered job.
        batch_params = {
            "JobDefinition": response_batch_register["jobDefinitionArn"],
            "JobName": response_batch_register["jobDefinitionName"],
        }

        put_rule_targets_aws_batch(
            cw_name,
            batch_params,
            config.AUDIENCE_ROUTER_JOB_ROLE_ARN,
            config.AUDIENCE_ROUTER_EXECUTION_ROLE_ARN,
        )

        self.scheduled = True

    def submit(self) -> None:
        """Submit a destination job

        Args:

        Returns:

        """

        # don't process if schedule set.
        if self.scheduled:
            return

        # Connect to AWS Batch
        if (
            self.aws_batch_connector is None
            and self.aws_batch_connector.job_def_name is not None
            and not isinstance(self.aws_batch_connector, AWSBatchConnector)
        ):
            raise Exception("Must register a job first.")

        # Submit the AWS batch job
        response_batch_submit = self.aws_batch_connector.submit_job()

        status = api_const.STATUS_DELIVERING
        if (
            response_batch_submit["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.OK.value
        ):
            status = db_const.AUDIENCE_STATUS_ERROR

        set_delivery_job_status(
            self.database,
            self.audience_delivery_job_id,
            status,
        )
        self.result = status


def get_destination_config(
    database: MongoClient,
    engagement_id: ObjectId,
    audience_id: ObjectId,
    destination: dict,
    audience_router_batch_size: int = 5000,
) -> DestinationBatchJob:
    """Get the configuration for the aws batch config of a destination.

    Args:
        database (MongoClient): The mongo database client.
        engagement_id (ObjectId): The ID of the engagement.
        audience_id (ObjectId): The ID of the audience.
        destination (dict): Destination object.
        audience_router_batch_size (int): Audience router AWS batch size.

    Returns:
        DestinationBatchJob: Destination batch job object.
    """

    audience_delivery_job = set_delivery_job(
        database,
        audience_id,
        destination[db_const.OBJECT_ID],
        [],
        engagement_id,
        destination.get(db_const.DELIVERY_PLATFORM_CONFIG),
    )

    delivery_platform = get_delivery_platform(
        database,
        destination[db_const.OBJECT_ID],
    )

    # get the configuration values
    config = get_config()

    # get destination specific env values
    ds_env_dict, ds_secret_dict = map_destination_credentials_to_dict(
        delivery_platform
    )

    # update the engagement latest delivery job
    try:
        add_delivery_job(
            database,
            engagement_id,
            audience_id,
            destination[db_const.OBJECT_ID],
            audience_delivery_job[db_const.ID],
        )
    except TypeError as exc:
        # mongomock does not support array_filters
        # but pymongo 3.6, MongoDB, and DocumentDB do.
        # log error, but keep process going.
        logging.error(exc)

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
        api_const.CDP_SERVICE_URL: config.CDP_SERVICE,
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
        delivery_platform[db_const.DELIVERY_PLATFORM_TYPE],
    )


def get_audience_destination_pairs(audiences: list) -> list:
    """function to get all the audience destination pairs for a list
    of audiences within an engagement.

    Args:
        audiences (list): list of audiences

    Returns:
        list: list of lists [[audience_id, destination_id],..]
    """

    if not audiences or not any(x for x in audiences if x):
        raise TypeError("Empty list provided.")

    # validate to ensure list of dicts has destinations
    if any(x for x in audiences if db_const.DESTINATIONS not in x):
        raise TypeError("must be a list of destinations.")

    return [
        [aud[db_const.OBJECT_ID], dest]
        for aud in audiences
        for dest in aud[db_const.DESTINATIONS]
        if isinstance(dest, dict)
    ]


if __name__ == "__main__":
    pass
