"""purpose of this file is to house all delivery related components.
 - delivery of an audience
"""
from http import HTTPStatus

from bson import ObjectId
from pymongo import MongoClient

from huxunifylib.database import constants as db_c
from huxunifylib.database.delivery_platform_management import (
    set_delivery_job,
    get_delivery_platform,
    set_delivery_job_status,
)
from huxunifylib.database.engagement_management import (
    add_delivery_job,
)
from huxunifylib.database.notification_management import create_notification
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
        self.result = status


# pylint: disable=too-many-locals
def get_destination_config(
    database: MongoClient,
    audience_id: ObjectId,
    destination: dict,
    engagement_id: ObjectId,
    username: str,
    replace_audience: bool = False,
) -> DestinationBatchJob:
    """Get the configuration for the aws batch config of a destination.

    Args:
        database (MongoClient): The mongo database client.
        audience_id (ObjectId): The ID of the audience.
        destination (dict): Destination object.
        engagement_id (ObjectId): The ID of the engagement.
        username (str): Username of user requesting to get the destination
            config.
        replace_audience(bool): Audience replacement flag

    Returns:
        DestinationBatchJob: Destination batch job object.

    Raises:
        FailedDestinationDependencyError: Failed to connect to a destination.
    """

    destination_id = (
        destination[db_c.OBJECT_ID]
        if db_c.OBJECT_ID in destination
        else destination[db_c.ID]
    )

    delivery_platform = get_delivery_platform(
        database,
        destination_id,
    )

    if not delivery_platform:
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_CRITICAL,
            (
                f'"Can not fetch destination {destination_id}" because '
                f"the destination does not exist."
            ),
            db_c.NOTIFICATION_CATEGORY_DESTINATIONS,
            username,
        )
        raise FailedDestinationDependencyError(
            destination_id, HTTPStatus.NOT_FOUND
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
        destination_id,
        [],
        username,
        replace_audience,
        engagement_id,
        destination.get(db_c.DELIVERY_PLATFORM_CONFIG),
    )

    # get the configuration values
    config = get_config()

    # get destination specific env values
    (
        destination_env_dict,
        destination_secret_dict,
    ) = map_destination_credentials_to_dict(delivery_platform)

    # get okta constant names used by audience router to communicate to CDM API.
    okta_env_dict, okta_secret_dict = get_okta_test_user_creds(config)

    # update the engagement latest delivery job
    try:
        add_delivery_job(
            database,
            engagement_id,
            audience_id,
            destination_id,
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
        MongoDBCredentials.MONGO_DB_HOST.name: config.MONGO_DB_HOST,
        MongoDBCredentials.MONGO_DB_PORT.name: str(config.MONGO_DB_PORT),
        MongoDBCredentials.MONGO_DB_USERNAME.name: config.MONGO_DB_USERNAME,
        MongoDBCredentials.MONGO_SSL_CERT.name: api_c.AUDIENCE_ROUTER_CERT_PATH,
        api_c.CDP_SERVICE: config.CDP_SERVICE,
        **destination_env_dict,
        **okta_env_dict,
    }

    # setup the secrets dict
    secret_dict = {
        MongoDBCredentials.MONGO_DB_PASSWORD.name: api_c.AUDIENCE_ROUTER_MONGO_PASSWORD_FROM,
        **destination_secret_dict,
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
        raise TypeError("Must be a list of destinations.")

    return [
        [aud[db_c.OBJECT_ID], dest]
        for aud in audiences
        for dest in aud[db_c.DESTINATIONS]
        if isinstance(dest, dict)
    ]


async def deliver_audience_to_destination(
    database: MongoClient,
    audience: dict,
    destination_id: ObjectId,
    user_name: str,
):
    """Async function that couriers delivery jobs.

    Args:
        database (MongoClient): The mongo database client.
        audience (dict): Audience object.
        destination_id (ObjectId): Destination ID.
        user_name (str): Username.
    """

    audience_id = audience[db_c.ID]

    # get destination object for delivering
    destination = get_delivery_platform(database, destination_id)
    if not destination:
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_CRITICAL,
            (
                f'Failed to delivered audience ID "{audience_id}" '
                f'to destination ID "{destination_id}" '
                f"because the destination does not exist."
            ),
            db_c.NOTIFICATION_CATEGORY_DELIVERY,
            user_name,
        )
        return

    replace_audience = False
    if destination.get(db_c.IS_AD_PLATFORM):
        replace_audience = list(
            map(
                lambda x: x[db_c.REPLACE_AUDIENCE],
                filter(
                    lambda x: (x[db_c.OBJECT_ID] == destination_id)
                    and db_c.REPLACE_AUDIENCE in x,
                    audience[db_c.DESTINATIONS],
                ),
            )
        )
        replace_audience = replace_audience[0] if replace_audience else None

    # set audience destination details dict into the destination object
    for aud_destination in audience.get(api_c.DESTINATIONS, []):
        if aud_destination[db_c.OBJECT_ID] == destination_id:
            destination = {**destination, **aud_destination}
            break

    delivery_job_id = str(
        create_delivery_job(
            database=database,
            audience_id=audience_id,
            destination=destination,
            engagement_id=db_c.ZERO_OBJECT_ID,
            username=user_name,
            replace_audience=replace_audience,
        )
    )

    logger.info(
        "Successfully created delivery job %s.",
        delivery_job_id,
    )

    # create notification
    create_notification(
        database,
        db_c.NOTIFICATION_TYPE_SUCCESS,
        (
            f'Successfully delivered audience "{audience[db_c.NAME]}" '
            f'to destination {destination[db_c.NAME]}".'
        ),
        db_c.NOTIFICATION_CATEGORY_DELIVERY,
        user_name,
    )


def create_delivery_job(
    database: MongoClient,
    audience_id: ObjectId,
    destination: dict,
    engagement_id: ObjectId,
    username: str,
    replace_audience: bool = False,
) -> ObjectId:
    """Create a delivery job with Pending status.

    Args:
        database (MongoClient): The mongo database client.
        audience_id (ObjectId): The ID of the audience.
        destination (dict): Destination object.
        engagement_id (ObjectId): The ID of the engagement.
        username (str): Username of user requesting to get the destination
            config.
        replace_audience(bool): Audience replacement flag

    Returns:
        ObjectId: Delivery Job ID.

    Raises:
        FailedDestinationDependencyError: Failed to connect to a destination.
    """

    destination_id = (
        destination[db_c.OBJECT_ID]
        if db_c.OBJECT_ID in destination
        else destination[db_c.ID]
    )

    delivery_platform = get_delivery_platform(
        database,
        destination_id,
    )

    if not delivery_platform:
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_CRITICAL,
            (
                f'"Can not fetch destination {destination_id}" because '
                f"the destination does not exist."
            ),
            db_c.NOTIFICATION_CATEGORY_DESTINATIONS,
            username,
        )
        raise FailedDestinationDependencyError(
            destination_id, HTTPStatus.NOT_FOUND
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
        destination_id,
        [],
        username,
        replace_audience,
        engagement_id,
        destination.get(db_c.DELIVERY_PLATFORM_CONFIG),
        db_c.PENDING,
    )

    # update the engagement latest delivery job
    try:
        add_delivery_job(
            database,
            engagement_id,
            audience_id,
            destination_id,
            audience_delivery_job[db_c.ID],
        )
    except TypeError as exc:
        # mongomock does not support array_filters
        # but pymongo 3.6, MongoDB, and DocumentDB do.
        # log error, but keep process going.
        logger.error(exc)

    return audience_delivery_job[db_c.ID]
