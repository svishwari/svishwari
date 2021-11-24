"""purpose of this file is to house all delivery related components.
 - delivery of an audience
"""
from http import HTTPStatus
from bson import ObjectId
from pymongo import MongoClient
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import constants as db_c
from huxunifylib.database.delivery_platform_management import (
    set_delivery_job,
    get_delivery_platform,
    set_delivery_job_status,
    set_job_in_pending_within_timeout_collection,
)
from huxunifylib.database.engagement_management import (
    add_delivery_job,
    check_active_engagement_deliveries,
)
from huxunifylib.connectors import AWSBatchConnector
from huxunifylib.util.general.const import (
    MongoDBCredentials,
    FacebookCredentials,
    SFMCCredentials,
    SendgridCredentials,
    GoogleCredentials,
    QualtricsCredentials,
)
from huxunifylib.util.audience_router.const import AudienceRouterConfig
from huxunifylib.util.general.logging import logger
from huxunify.api import constants as api_c
from huxunify.api.config import get_config, Config
from huxunify.api.data_connectors.aws import (
    set_cloud_watch_rule,
    put_rule_targets_aws_batch,
    CloudWatchState,
)
from huxunify.api.exceptions.integration_api_exceptions import (
    FailedDestinationDependencyError,
)


def map_destination_credentials_to_dict(destination: dict) -> tuple:
    """Map destination credentials to a dictionary for aws batch.
    Handle any custom logic here in the future for new destination types.

    Args:
        destination (dict): The destination object.

    Returns:
        tuple: The credential tuple for (env, secrets).

    Raises:
        KeyError: Exception when the key is missing in the object.
    """

    # skip if no authentication details provided.
    if db_c.DELIVERY_PLATFORM_AUTH not in destination:
        raise KeyError(
            f"No authentication details for {destination[db_c.DELIVERY_PLATFORM_NAME]}"
        )

    # get auth
    auth = destination[db_c.DELIVERY_PLATFORM_AUTH]

    if (
        destination[db_c.DELIVERY_PLATFORM_TYPE]
        == db_c.DELIVERY_PLATFORM_FACEBOOK
    ):
        env_dict = {
            FacebookCredentials.FACEBOOK_AD_ACCOUNT_ID.name: auth[
                api_c.FACEBOOK_AD_ACCOUNT_ID
            ],
            FacebookCredentials.FACEBOOK_APP_ID.name: auth[
                api_c.FACEBOOK_APP_ID
            ],
        }
        secret_dict = {
            FacebookCredentials.FACEBOOK_ACCESS_TOKEN.name: auth[
                api_c.FACEBOOK_ACCESS_TOKEN
            ],
            FacebookCredentials.FACEBOOK_APP_SECRET.name: auth[
                api_c.FACEBOOK_APP_SECRET
            ],
        }

    elif (
        destination[db_c.DELIVERY_PLATFORM_TYPE] == db_c.DELIVERY_PLATFORM_SFMC
    ):
        env_dict = {
            SFMCCredentials.SFMC_CLIENT_ID.name: auth[api_c.SFMC_CLIENT_ID],
            SFMCCredentials.SFMC_AUTH_URL.name: auth[api_c.SFMC_AUTH_BASE_URI],
            SFMCCredentials.SFMC_ACCOUNT_ID.name: auth[api_c.SFMC_ACCOUNT_ID],
            SFMCCredentials.SFMC_SOAP_ENDPOINT.name: auth[
                api_c.SFMC_SOAP_BASE_URI
            ],
            SFMCCredentials.SFMC_URL.name: auth[api_c.SFMC_REST_BASE_URI],
        }

        secret_dict = {
            SFMCCredentials.SFMC_CLIENT_SECRET.name: auth[
                api_c.SFMC_CLIENT_SECRET
            ]
        }
    elif destination[db_c.DELIVERY_PLATFORM_TYPE] in [
        db_c.DELIVERY_PLATFORM_SENDGRID,
        db_c.DELIVERY_PLATFORM_TWILIO,
    ]:
        env_dict = {}
        secret_dict = {
            SendgridCredentials.SENDGRID_AUTH_TOKEN.name: auth[
                api_c.SENDGRID_AUTH_TOKEN
            ]
        }

    elif (
        destination[db_c.DELIVERY_PLATFORM_TYPE]
        == db_c.DELIVERY_PLATFORM_QUALTRICS
    ):
        env_dict = {
            QualtricsCredentials.QUALTRICS_DATA_CENTER.name: auth[
                api_c.QUALTRICS_DATA_CENTER
            ],
            QualtricsCredentials.QUALTRICS_OWNER_ID.name: auth[
                api_c.QUALTRICS_OWNER_ID
            ],
            QualtricsCredentials.QUALTRICS_DIRECTORY_ID.name: auth[
                api_c.QUALTRICS_DIRECTORY_ID
            ],
        }

        secret_dict = {
            QualtricsCredentials.QUALTRICS_API_TOKEN.name: auth[
                api_c.QUALTRICS_API_TOKEN
            ]
        }

    elif (
        destination[db_c.DELIVERY_PLATFORM_TYPE]
        == db_c.DELIVERY_PLATFORM_GOOGLE
    ):
        env_dict = {
            GoogleCredentials.GOOGLE_CLIENT_CUSTOMER_ID.name: auth[
                api_c.GOOGLE_CLIENT_CUSTOMER_ID
            ],
        }

        secret_dict = {
            GoogleCredentials.GOOGLE_DEVELOPER_TOKEN.name: auth[
                api_c.GOOGLE_DEVELOPER_TOKEN
            ],
            GoogleCredentials.GOOGLE_CLIENT_ID.name: auth[
                api_c.GOOGLE_CLIENT_ID
            ],
            GoogleCredentials.GOOGLE_REFRESH_TOKEN.name: auth[
                api_c.GOOGLE_REFRESH_TOKEN
            ],
            GoogleCredentials.GOOGLE_CLIENT_SECRET.name: auth[
                api_c.GOOGLE_CLIENT_SECRET
            ],
        }
    else:
        raise KeyError(
            f"No configuration for destination type: {destination[db_c.DELIVERY_PLATFORM_TYPE]}"
        )

    return env_dict, secret_dict


def get_okta_test_user_creds(config: Config) -> tuple:
    """Pass in SSM Store values for the OKTA test user params.

    Args:
        config (Config): Config object to get the current OKTA Issue/Client.

    Returns:
        dict: tuple: The credential tuple for (env, secrets).
    """

    # only return the constant names, they are used in the Audience Router
    # to retrieve the actual secrets from AWS SSM

    return {
        api_c.OKTA_ISSUER: config.OKTA_ISSUER,
        api_c.OKTA_CLIENT_ID: config.OKTA_CLIENT_ID,
    }, {
        api_c.OKTA_TEST_USER_NAME: api_c.UNIFIED_OKTA_TEST_USER_NAME,
        api_c.OKTA_TEST_USER_PW: api_c.UNIFIED_OKTA_TEST_USER_PW,
        api_c.OKTA_REDIRECT_URI: api_c.UNIFIED_OKTA_REDIRECT_URI,
    }


# pylint: disable=too-many-instance-attributes,too-many-arguments
class DestinationBatchJob:
    """Class for housing the Destination batch config."""

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
        logger.info("Connecting to AWS Batch.")
        if aws_batch_connector is None:
            aws_batch_connector = AWSBatchConnector(
                job_head_name,
                self.audience_delivery_job_id,
            )
        self.aws_batch_connector = aws_batch_connector
        logger.info("Connected to AWS Batch.")

        # get the configuration values
        config = get_config()

        # Register AWS batch job
        logger.info("Registering AWS Batch job.")
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
            logger.error(
                "Failed to Register AWS Batch job for delivery job ID %s.",
                self.audience_delivery_job_id,
            )
            set_delivery_job_status(
                self.database,
                self.audience_delivery_job_id,
                db_c.AUDIENCE_STATUS_ERROR,
            )
            self.result = db_c.AUDIENCE_STATUS_ERROR
            return
        logger.info(
            "Successfully Registered AWS Batch job for %s.",
            self.audience_delivery_job_id,
        )
        self.result = db_c.AUDIENCE_STATUS_DELIVERING

        # check if engagement has a delivery flight schedule set
        if not (
            engagement_doc and engagement_doc.get(api_c.DELIVERY_SCHEDULE)
        ):
            logger.warning(
                "Delivery schedule is not set for %s.",
                engagement_doc[db_c.ID],
            )
            return

        # create the rule name
        cw_name = f"{engagement_doc[db_c.ID]}-{self.destination_type}"

        # TODO hookup converted cron job expression HUS-794
        if not set_cloud_watch_rule(
            cw_name,
            "cron(15 0 * * ? *)",
            config.AUDIENCE_ROUTER_JOB_ROLE_ARN,
        ):
            logger.error(
                "Error creating cloud watch rule for engagement with ID %s.",
                engagement_doc[db_c.ID],
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
            self.audience_delivery_job_id,
            config.AUDIENCE_ROUTER_EXECUTION_ROLE_ARN,
            config.AUDIENCE_ROUTER_JOB_QUEUE,
        )

        self.scheduled = True

    def submit(self) -> None:
        """Submit a destination job

        Args:

        Returns:

        Raises:
            Exception: Exception raised if a job is missing.
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

        status = api_c.STATUS_DELIVERING
        if (
            response_batch_submit["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.OK.value
        ):
            logger.error(
                "Failed to Submit AWS Batch job for %s.",
                self.audience_delivery_job_id,
            )
            status = db_c.AUDIENCE_STATUS_ERROR

        set_delivery_job_status(
            self.database,
            self.audience_delivery_job_id,
            status,
        )

        # Add delivery job id to pending_within_timeout, if status is not
        # delivering.
        if status == api_c.STATUS_DELIVERING:
            set_job_in_pending_within_timeout_collection(
                self.database, self.audience_delivery_job_id
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

    Raises:
        FailedDestinationDependencyError: Failed to connect to a destination.
    """

    delivery_platform = get_delivery_platform(
        database,
        destination[db_c.OBJECT_ID],
    )

    # validate destination status first.
    if (
        delivery_platform.get(db_c.DELIVERY_PLATFORM_STATUS)
        != db_c.STATUS_SUCCEEDED
    ):
        logger.error(
            "%s authentication failed.", delivery_platform.get(db_c.NAME)
        )
        raise FailedDestinationDependencyError(
            delivery_platform[api_c.NAME], HTTPStatus.FAILED_DEPENDENCY
        )

    audience_delivery_job = set_delivery_job(
        database,
        audience_id,
        destination[db_c.OBJECT_ID],
        [],
        engagement_id,
        destination.get(db_c.DELIVERY_PLATFORM_CONFIG),
    )

    # get the configuration values
    config = get_config()

    # get destination specific env values
    ds_env_dict, ds_secret_dict = map_destination_credentials_to_dict(
        delivery_platform
    )

    # get okta constant names used by audience router to communicate to CDM API.
    okta_env_dict, okta_secret_dict = get_okta_test_user_creds(config)

    # update the engagement latest delivery job
    try:
        add_delivery_job(
            database,
            engagement_id,
            audience_id,
            destination[db_c.OBJECT_ID],
            audience_delivery_job[db_c.ID],
        )
    except TypeError as exc:
        # mongomock does not support array_filters
        # but pymongo 3.6, MongoDB, and DocumentDB do.
        # log error, but keep process going.
        logger.error(exc)

    # Setup AWS Batch env dict
    env_dict = {
        AudienceRouterConfig.DELIVERY_JOB_ID.name: str(
            audience_delivery_job[db_c.ID]
        ),
        AudienceRouterConfig.BATCH_SIZE.name: str(audience_router_batch_size),
        MongoDBCredentials.MONGO_DB_HOST.name: config.MONGO_DB_HOST,
        MongoDBCredentials.MONGO_DB_PORT.name: str(config.MONGO_DB_PORT),
        MongoDBCredentials.MONGO_DB_USERNAME.name: config.MONGO_DB_USERNAME,
        MongoDBCredentials.MONGO_SSL_CERT.name: api_c.AUDIENCE_ROUTER_CERT_PATH,
        api_c.CDP_SERVICE: config.CDP_SERVICE,
        **ds_env_dict,
        **okta_env_dict,
    }

    # setup the secrets dict
    secret_dict = {
        MongoDBCredentials.MONGO_DB_PASSWORD.name: api_c.AUDIENCE_ROUTER_MONGO_PASSWORD_FROM,
        **ds_secret_dict,
        **okta_secret_dict,
    }

    return DestinationBatchJob(
        database,
        audience_delivery_job[db_c.ID],
        secret_dict,
        env_dict,
        delivery_platform[db_c.DELIVERY_PLATFORM_TYPE],
    )


def get_audience_destination_pairs(audiences: list) -> list:
    """function to get all the audience destination pairs for a list
    of audiences within an engagement.

    Args:
        audiences (list): list of audiences

    Returns:
        list: list of lists [[audience_id, destination_id],..]

    Raises:
        TypeError: Raised when an empty list is provided.
    """

    if not audiences or not any(x for x in audiences if x):
        raise TypeError("Empty list provided.")

    # validate to ensure list of dicts has destinations
    if any(x for x in audiences if db_c.DESTINATIONS not in x):
        raise TypeError("must be a list of destinations.")

    return [
        [aud[db_c.OBJECT_ID], dest]
        for aud in audiences
        for dest in aud[db_c.DESTINATIONS]
        if isinstance(dest, dict)
    ]


def toggle_event_driven_routers(
    database: DatabaseClient,
    state: CloudWatchState = None,
    routers: list = None,
) -> None:
    """Toggle event driven routers in cloudwatch.

    Args:
        database (DatabaseClient): Mongo database client.
        state (CloudWatchState): Cloudwatch toggle state enum.
        routers (list): List of router names to toggle.

    Returns:

    """

    # grab default routers if not provided.
    routers = get_config().EVENT_ROUTERS if routers is None else routers

    # get all the active engagements
    active_engagements = check_active_engagement_deliveries(database)

    if state is None:
        # set state based on active engagements
        # if there are active engagements, the router should be enabled.
        state = (
            CloudWatchState.ENABLE
            if active_engagements
            else CloudWatchState.DISABLE
        )

    # TODO - hookup after ORCH-401 deploys the FLDR and CPDR to a cloud watch event.
    # # toggle the routers
    # _ = [toggle_cloud_watch_rule(x, state) for x in routers]


if __name__ == "__main__":
    pass
