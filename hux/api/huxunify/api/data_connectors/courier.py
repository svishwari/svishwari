"""
purpose of this file is to house all delivery related components.
 - delivery of an audience
"""
from http import HTTPStatus
from bson import ObjectId
from huxunifylib.database import constants as db_const
from huxunifylib.database.delivery_platform_management import (
    set_delivery_job,
    get_delivery_platform,
    set_delivery_job_status,
)
from huxunifylib.database.data_management import get_constant
from huxunifylib.connectors.aws_batch_connector import AWSBatchConnector
from huxunify.api.route.utils import get_db_client
from huxunify.api import config, constants as api_const


def map_destination_credentials_to_dict(destination: dict) -> dict:
    """Map destination credentials to a dictionary for aws batch.

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
        # TODO - hook up engagements once done in SPRINT 8
        self.engagement_id = engagement_id
        # simulate until we hook up the engagement audiences using lookup.
        self.audience_ids = [ObjectId, ObjectId]
        self.db_client = db_client

    def delivery_route(self, audience_ids: list = None):
        """Set up the delivery route for an engagement's audiences.

        Args:
            audience_ids (list): List of audience IDs.

        Returns:
            bool: If the delivery job was successfully initiated.
        """

        # use audiences unless passed in
        audience_ids = audience_ids if audience_ids else self.audience_ids

        # prep all the audiences for delivery
        for audience_id in audience_ids:
            # grab all the destination ids that audience must be delivered to.
            # TODO - populate using mongo lookups.
            destination_ids = [ObjectId, ObjectId]
            for destination_id in destination_ids:
                self._process_destination(destination_id, audience_id)

    def _process_destination(self, destination_id, audience_id) -> None:
        """Process a destination for submitting to AWS Batch.

        Args:
            destination_id (ObjectId): The ID of the destination.
            audience_id (ObjectId): The ID of the audience.

        Returns:

        """
        audience_delivery_job = set_delivery_job(
            self.db_client, audience_id, destination_id, []
        )

        audience_router_batch_size = get_constant(
            self.db_client,
            db_const.AUDIENCE_ROUTER_BATCH_SIZE,
        )

        aws_batch_mem_limit = int(
            get_constant(
                self.db_client,
                db_const.AWS_BATCH_MEM_LIMIT,
            )
        )

        delivery_platform = get_delivery_platform(
            self.db_client,
            destination_id,
        )

        # Setup AWS Batch env vars and secrets
        aws_env_dict = {
            db_const.DELIVERY_JOB_ID.upper(): str(
                audience_delivery_job[db_const.ID]
            ),
            api_const.BATCH_SIZE.upper(): str(
                audience_router_batch_size[db_const.CONSTANT_VALUE]
            ),
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

        self.submit_batch_job(
            audience_delivery_job[db_const.ID],
            aws_secret_dict,
            aws_env_dict,
            aws_batch_mem_limit,
        )

    def submit_batch_job(
        self,
        audience_delivery_job_id: ObjectId,
        aws_secret_dict: dict,
        aws_env_dict: dict,
        aws_batch_mem_limit: int,
        job_head_name: str = "audiencerouter",
    ) -> None:
        """Process a destination for submitting to AWS Batch.

        Args:
            audience_delivery_job_id (ObjectId): The ID of the audience
                delivery job.
            aws_secret_dict (dict): The aws secret dict passed to aws batch.
            aws_env_dict (dict): The aws env dict passed to aws batch.
            aws_batch_mem_limit (int): The aws batch memory limit.
            job_head_name (str): The name of the aws batch job head name.
        Returns:

        """
        # Connect to AWS Batch
        aws_batch_connector = AWSBatchConnector(
            job_head_name,
            audience_delivery_job_id,
        )

        # Register AWS batch job
        response_batch_register = aws_batch_connector.register_job(
            job_role_arn=config.AUDIENCE_ROUTER_JOB_ROLE_ARN.name,
            exec_role_arn=config.AUDIENCE_ROUTER_EXECUTION_ROLE_ARN,
            exec_image=config.AUDIENCE_ROUTER_IMAGE,
            env_dict=aws_env_dict,
            secret_dict=aws_secret_dict,
            aws_batch_mem_limit=aws_batch_mem_limit,
        )

        if (
            response_batch_register["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.OK.value
        ):
            set_delivery_job_status(
                self.db_client,
                audience_delivery_job_id,
                db_const.STATUS_FAILED,
            )
            return

        # Submit the AWS batch job
        response_batch_submit = aws_batch_connector.submit_job()

        status = db_const.STATUS_IN_PROGRESS
        if (
            response_batch_submit["ResponseMetadata"]["HTTPStatusCode"]
            != HTTPStatus.OK.value
        ):
            status = db_const.STATUS_FAILED

        set_delivery_job_status(
            self.db_client, audience_delivery_job_id, status
        )


if __name__ == "__main__":
    pass
