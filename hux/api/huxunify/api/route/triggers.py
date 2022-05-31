"""Paths for triggers API"""
from flask import Blueprint, Response
from huxunifylib.database import constants as db_c
from huxunifylib.database.collection_management import get_documents
from huxunify.api.route.utils import get_db_client
from huxunify.api import constants as api_c


triggers_bp = Blueprint(f"/{api_c.TRIGGERS_TAG}", import_name=__name__)


@triggers_bp.route(
    f"/{api_c.TRIGGERS_TAG}/{api_c.DELIVERIES}/{api_c.PENDING_JOBS}",
    methods=["GET"],
)
def pending_jobs() -> Response:
    """Purpose of this function is to return all pending jobs for
    the metrics KEDA API.

    Returns:
        Response: json response with count
    """

    # get pending jobs from the database.
    return {
        api_c.DELIVERIES: {
            api_c.PENDING_JOBS: get_documents(
                get_db_client(),
                db_c.DELIVERY_JOBS_COLLECTION,
                {db_c.STATUS: db_c.STATUS_PENDING},
            ).get(api_c.TOTAL_RECORDS, 0)
        }
    }