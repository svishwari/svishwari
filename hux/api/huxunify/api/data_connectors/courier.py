"""
purpose of this file is to house all delivery related components.
 - delivery of an audience
"""


"""Controller for functionality related to audience delivery."""
import datetime
import logging
from http import HTTPStatus
from operator import attrgetter
from bson import ObjectId
from typing import Tuple, List
from huxunifylib.database import constants as db_const
from huxunifylib.database.delivery_platform_management import set_delivery_job, get_delivery_platform
from huxunifylib.database.data_management import get_constant
from huxunify.api.route.utils import get_db_client

# import connexion
# from connexion import ProblemException
# from huxadv.util.general.const import FacebookCredentials
# from huxadv.connectors import constants as conn_const
# 
# from huxunifylib.database import (
#     constants,
#     audience_management,
#     data_management,
#     delivery_platform_management,
# )
# from huxadv.connectors.aws_batch_connector import AWSBatchConnector
# 
# from huxadv.util.general.const import (
#     MongoDBCredentials,
#     AudienceRouterInfrastructure,
#     HuxAdvException,
#     MonitoringAlerting,
# )
# from huxadv.util.general.connector_util import get_delivery_platform_connector
# 
# from api import const, transform_api
# from api.controllers.util import time_diff_hours, fetch_auth_secrets
# from api.models import (
#     AudienceDeliveryJob,
#     AudienceDeliveryJobPost,
# )
# from api.controllers import util
# 
# 
# def fetch_audience_config_dp(
#     delivery_platform_id: ObjectId, audience_id: ObjectId
# ) -> dict:
#     """Fetch audience configuration from delivery platform.
#     Args:
#         delivery_platform_id (ObjectId): The ID of the delivery platform.
#         audience_id (ObjectId): The ID of the audience.
# 
#      Returns:
#          dict: Retrieved audience configuration from delivery platform.
#     """
#     delivery_platform = delivery_platform_management.get_delivery_platform(
#         database=util.get_db_client(),
#         delivery_platform_id=delivery_platform_id,
#     )
# 
#     audience = audience_management.get_audience_config(
#         database=util.get_db_client(), audience_id=audience_id
#     )
# 
#     auth_details_secrets = fetch_auth_secrets(delivery_platform)
# 
#     dp_connector = get_delivery_platform_connector(
#         platform_type=delivery_platform[constants.DELIVERY_PLATFORM_TYPE],
#         auth_details_secrets=auth_details_secrets,
#     )
#     try:
#         audience_config = dp_connector.get_audience_config(
#             audience[constants.AUDIENCE_NAME]
#         )
# 
#     except HuxAdvException as exc:
#         logging.error(
#             "%s: [%s: %s]",
#             const.CANNOT_FETCH_AUD_CONFIG_CONNECTOR,
#             exc.__class__,
#             exc,
#         )
#         raise ProblemException(
#             status=int(HTTPStatus.BAD_REQUEST.value),
#             title=HTTPStatus.BAD_REQUEST.description,
#             detail=f"{const.CANNOT_FETCH_AUD_CONFIG_CONNECTOR}.",
#         ) from exc
#     except Exception as exc:
#         logging.error(
#             "%s: [%s: %s]",
#             const.CANNOT_FETCH_AUD_CONFIG_DP_API,
#             exc.__class__,
#             exc,
#         )
#         raise ProblemException(
#             status=int(HTTPStatus.BAD_REQUEST.value),
#             title=HTTPStatus.BAD_REQUEST.description,
#             detail=f"{const.CANNOT_FETCH_AUD_CONFIG_DP_API}.",
#         ) from exc
# 
#     return audience_config
# 
# 
# def get_all_audience_delivery_jobs(
#     audience_id: str,
# ) -> Tuple[List[AudienceDeliveryJob], HTTPStatus]:
#     """Get all audience delivery jobs.
# 
#     Args:
#         audience_id (str): The ID of the audience.
# 
#     Returns:
#         Tuple[List[AudienceDeliveryJob], HTTPStatus]:
#             List of audience delivery jobs, HTTP Status.
#     """
#     find = connexion.request.args.get("find")
# 
#     if not find:
#         audience_delivery_jobs = (
#             delivery_platform_management.get_delivery_jobs(
#                 database=util.get_db_client(),
#                 audience_id=ObjectId(audience_id),
#             )
#         )
# 
#     if find == "recent":
#         delivery_platform_ids = (
#             delivery_platform[constants.ID]
#             for delivery_platform in (
#                 delivery_platform_management.get_all_delivery_platforms(
#                     database=util.get_db_client(),
#                 )
#             )
#         )
# 
#         audience_delivery_jobs = []
#         for delivery_platform_id in delivery_platform_ids:
#             recent_job = (
#                 delivery_platform_management.get_audience_recent_delivery_job(
#                     database=util.get_db_client(),
#                     audience_id=ObjectId(audience_id),
#                     delivery_platform_id=delivery_platform_id,
#                 )
#             )
# 
#             curr_time = datetime.datetime.utcnow()
# 
#             if not recent_job:
#                 continue
# 
#             # fetch audience in delivery platform when the delivery job has
#             # delivery status of "Succeeded" AND
#             # some time has elapsed since delivering (eg. 24 hours)
#             if recent_job.get(constants.JOB_END_TIME):
#                 if (
#                     time_diff_hours(
#                         curr_time, recent_job.get(constants.JOB_END_TIME)
#                     )
#                     > 24
#                     and recent_job[constants.JOB_STATUS]
#                     == constants.STATUS_SUCCEEDED
#                 ):
#                     # fetch audience in the delivery platform
#                     audience_config = fetch_audience_config_dp(
#                         delivery_platform_id, ObjectId(audience_id)
#                     )
# 
#                     # check the audience status code and return the delivery
#                     # status for the audience in the platform
#                     status_code = audience_config[
#                         conn_const.AUDIENCE_DELIVERY_STATUS
#                     ][conn_const.AUDIENCE_DELIVERY_STATUS_CODE]
# 
#                     if (
#                         status_code
#                         == conn_const.AUDIENCE_DELIVERY_STATUS_CODE_READY
#                     ):
#                         # set audience size in the database, if the audience is ready
#                         recent_job = delivery_platform_management.set_delivery_job_audience_size(
#                             database=util.get_db_client(),
#                             delivery_job_id=recent_job[constants.ID],
#                             audience_size=audience_config[
#                                 conn_const.AUDIENCE_SIZE
#                             ],
#                         )
# 
#                         status = conn_const.AUDIENCE_DELIVERY_STATUS_READY
#                     elif (
#                         status_code
#                         == conn_const.AUDIENCE_DELIVERY_STATUS_CODE_INACTIVE
#                     ):
#                         status = conn_const.AUDIENCE_DELIVERY_STATUS_INACTIVE
#                     elif (
#                         status_code
#                         == conn_const.AUDIENCE_DELIVERY_STATUS_CODE_ERROR
#                     ):
#                         status = conn_const.AUDIENCE_DELIVERY_STATUS_ERROR
#                     else:
#                         status = (
#                             conn_const.AUDIENCE_DELIVERY_STATUS_UNAVAILABLE
#                         )
# 
#                     recent_job[const.AUDIENCE_DELIVERY_STATUS] = status
# 
#             audience_delivery_jobs.append(recent_job)
# 
#     response = [
#         transform_api.audience_delivery_job_api(audience_delivery_job)
#         for audience_delivery_job in audience_delivery_jobs
#         if audience_delivery_job
#     ]
# 
#     return response, HTTPStatus.OK
# 
# 
# def get_audience_delivery_job(
#     audience_id: str, delivery_job_id: str  # pylint: disable=W0613
# ) -> Tuple[AudienceDeliveryJob, HTTPStatus]:
#     """Get an audience delivery job by ID.
# 
#     Args:
#         delivery_job_id (str): The ID of the delivery job.
# 
#     Returns:
#         Tuple[AudienceDeliveryJob, HTTPStatus]:
#             Audience delivery job, HTTP Status.
#     """
# 
#     audience_delivery_job = delivery_platform_management.get_delivery_job(
#         database=util.get_db_client(),
#         delivery_job_id=ObjectId(delivery_job_id),
#     )
# 
#     response = transform_api.audience_delivery_job_api(audience_delivery_job)
# 
#     return response, HTTPStatus.OK


def get_env_dict():
    return {
        **util.get_mongo_db_env_dict(),
        **util.get_audience_router_env_dict(),
        **util.get_monitoring_env_dict(),
    }

def get_env_vars():
    return {
        **util.get_mongo_db_env_dict(),
        **util.get_audience_router_env_dict(),
        **util.get_monitoring_env_dict(),
    }

class Courier:
    """
    Courier that delivers audiences. Tips optional.
    """

    def __init__(self, engagement_id: ObjectId, db_client=get_db_client()):
        """
        init method for the courier
        """
        # TODO - hook up engagements once done in SPRINT 8
        self.engagement_id = ObjectId
        # simulate until we hook up the engagement audiences using lookup.
        self.audience_ids = [ObjectId, ObjectId]
        self.db_client = db_client

    def delivery_route(self, audience_ids: list=[]):
        """
        deliver
        Returns:
        """

        # use audiences unless passed in
        audiences = audience_ids if audience_ids else self.audience_ids

        # prep all the audiences for delivery
        for audience_id in audience_ids:
            # grab all the destination ids that audience must be delivered to.
            destination_ids = [ObjectId, ObjectId]
            for destination_id in destination_ids:
                self._process_destination(destination_id, audience_id)

    def _process_destination(self, destination_id, audience_id):
        # assign the delivery job
        audience_delivery_job = set_delivery_job(
            self.db_client,
            audience_id,
            destination_id
        )
        
        response_set_job = transform_api.audience_delivery_job_api(
            audience_delivery_job
        )

        audience_router_batch_size = get_constant(
            self.db_client,
            db_const.AUDIENCE_ROUTER_BATCH_SIZE,
        )

        aws_batch_mem_limit = get_constant(
            self.db_client,
            db_const.AWS_BATCH_MEM_LIMIT,
        )

        delivery_platform = get_delivery_platform(
            self.db_client,
            destination_id,
        )


    def _deliver(self, audience_id):
        audience_delivery_job = set_delivery_job(self.db_client,
            self.engagement_id, audience_id,
            delivery_platform_id=ObjectId(delivery_platform_id),
            delivery_platform_generic_campaigns=None,
        )


if __name__ == '__main__':
    pass
