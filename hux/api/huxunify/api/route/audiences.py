"""
Paths for Orchestration API
"""
import csv
from datetime import datetime
from http import HTTPStatus
from pathlib import Path
from typing import Tuple
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, Response

from huxunifylib.connectors import connector_cdp
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database import (
    orchestration_management,
)
import huxunifylib.database.constants as db_c

from huxunify.api.config import get_config
from huxunify.api.schema.utils import AUTH401_RESPONSE
import huxunify.api.constants as api_c
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    get_user_name,
    api_error_handler,
)
from huxunify.api.route.utils import get_db_client

# setup the audiences blueprint
audience_bp = Blueprint(api_c.AUDIENCE_ENDPOINT, import_name=__name__)


@audience_bp.before_request
@secured()
def before_request():
    """Protect all of the audiences endpoints."""
    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    audience_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>/<download_type>",
    "AudienceDownloadView",
)
class AudienceDownload(SwaggerView):
    """
    Audience Put view class
    """

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": api_c.DOWNLOAD_TYPE,
            "description": "Download Type",
            "type": "string",
            "in": "path",
            "required": True,
            "example": api_c.GOOGLE_ADS,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Download Audience.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to download audience.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @get_user_name()
    def get(
        self, audience_id: str, download_type: str, user_name: str
    ) -> Tuple[Response, int]:
        """Downloads an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            download_type (str): Download type.
            user_name (str): User name.

        Returns:
            Tuple[Response, int]: File Object Response, HTTP status.

        """
        if not api_c.DOWNLOAD_TYPES.get(download_type):
            return {"message": "Invalid download type"}, HTTPStatus.BAD_REQUEST

        database = get_db_client()
        audience = orchestration_management.get_audience(
            database, ObjectId(audience_id)
        )

        if not audience:
            return {
                "message": api_c.AUDIENCE_NOT_FOUND
            }, HTTPStatus.BAD_REQUEST

        cdp = connector_cdp.ConnectorCDP(get_config().CDP_SERVICE)
        column_set = [api_c.HUX_ID] + list(
            api_c.DOWNLOAD_TYPES[download_type].keys()
        )
        data_batches = cdp.read_batches(
            location_details={
                api_c.AUDIENCE_FILTERS: audience.get(api_c.AUDIENCE_FILTERS),
            },
            batch_size=int(api_c.CUSTOMERS_DEFAULT_BATCH_SIZE),
            column_set=column_set,
        )

        audience_file_name = (
            f"{datetime.now().strftime('%m%d%Y%H%M%S')}"
            f"_{audience_id}_{download_type}.csv"
        )

        with open(
            audience_file_name, "w", newline="", encoding="utf-8"
        ) as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(api_c.DOWNLOAD_TYPES[download_type].values())
            for dataframe_batch in data_batches:
                dataframe_batch.to_csv(
                    csvfile,
                    mode="a",
                    index=False,
                    columns=list(api_c.DOWNLOAD_TYPES[download_type].keys()),
                    header=False,
                )

        audience_file = Path(audience_file_name)
        data = audience_file.read_bytes()
        audience_file.unlink()

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            f"{user_name} downloaded the audience, {audience[db_c.NAME]}"
            f" with format {download_type}.",
            api_c.ORCHESTRATION_TAG,
        )

        return (
            Response(
                data,
                headers={
                    "Content-Type": "application/csv",
                    "Content-Disposition": "attachment; filename=%s;"
                    % audience_file_name,
                },
            ),
            HTTPStatus.OK,
        )
