"""Return structures file for Hux API endpoints"""
# pylint: disable=invalid-name
from http import HTTPStatus
from typing import Tuple, Union

from flask import Response, jsonify
from flask_marshmallow import Schema

from huxunify.api import constants as api_c


class HuxResponse:
    """Utility class to hold all response functions"""

    # 2XX response codes
    @staticmethod
    def OK(
        message: str = None,
        data: Union[dict, list] = None,
        data_schema: Schema = None,
        extra_fields: dict = None,
    ) -> Tuple[Response, int]:
        """OK (200)
        Args:
            message (str): Message to be returned.
            data (dict): Data to be returned.
            data_schema (Schema): Schema for the data.
            extra_fields (dict): dict containing any additional body parameters.
        Returns:
            Tuple[Response, int]: Response entity, response code
        """
        return HuxResponse.response(
            HTTPStatus.OK, message, data, data_schema, extra_fields
        )

    @staticmethod
    def CREATED(
        message: str = None,
        data: Union[dict, list] = None,
        data_schema: Schema = None,
        extra_fields: dict = None,
    ) -> Tuple[Response, int]:
        """Created (201)
        Args:
            message (str): Message to be returned.
            data (Union[dict, list]): Data to be returned.
            data_schema (Schema): Schema for the data.
            extra_fields (dict): dict containing any additional body parameters.
        Returns:
            Tuple[Response, int]: Response entity, response code
        """
        return HuxResponse.response(
            HTTPStatus.CREATED, message, data, data_schema, extra_fields
        )

    @staticmethod
    def ACCEPTED(
        message: str = None,
        data: Union[dict, list] = None,
        data_schema: Schema = None,
        extra_fields: dict = None,
    ) -> Tuple[Response, int]:
        """Accepted (202)
        Args:
            message (str): Message to be returned.
            data (Union[dict, list]): Data to be returned.
            data_schema (Schema): Schema for the data.
            extra_fields (dict): dict containing any additional body parameters.
        Returns:
            Tuple[Response, int]: Response entity, response code
        """
        return HuxResponse.response(
            HTTPStatus.ACCEPTED, message, data, data_schema, extra_fields
        )

    @staticmethod
    def NO_CONTENT() -> Tuple[Response, int]:
        """Non content (204)
        Returns:
            Tuple[Response, int]: Response entity, response code
        """
        return jsonify({}), HTTPStatus.NO_CONTENT

    # 4XX Response codes
    @staticmethod
    def BAD_REQUEST(
        message: str = None, extra_fields: dict = None
    ) -> Tuple[Response, int]:
        """Bad request (400)
        Args:
            message (str): Message to be returned.
            extra_fields (dict): dict containing any additional body parameters.
        Returns:
            Tuple[Response, int]: Response entity, response code
        """
        return HuxResponse.response(
            HTTPStatus.BAD_REQUEST, message, None, None, extra_fields
        )

    @staticmethod
    def UNAUTHORIZED(
        message: str = None, extra_fields: dict = None
    ) -> Tuple[Response, int]:
        """Unauthorized (401)
        Args:
            message (str): Message to be returned.
            extra_fields (dict): dict containing any additional body parameters.
        Returns:
            Tuple[Response, int]: Response entity, response code
        """
        return HuxResponse.response(
            HTTPStatus.UNAUTHORIZED, message, None, None, extra_fields
        )

    @staticmethod
    def FORBIDDEN(
        message: str = None, extra_fields: dict = None
    ) -> Tuple[Response, int]:
        """Forbidden (403)
        Args:
            message (str): Message to be returned.
            extra_fields (dict): dict containing any additional body parameters.
        Returns:
            Tuple[Response, int]: Response entity, response code
        """
        return HuxResponse.response(
            HTTPStatus.FORBIDDEN, message, None, None, extra_fields
        )

    @staticmethod
    def NOT_FOUND(
        message: str = None, extra_fields: dict = None
    ) -> Tuple[Response, int]:
        """Not found (404)
        Args:
            message (str): Message to be returned.
            extra_fields (dict): dict containing any additional body parameters.
        Returns:
            Tuple[Response, int]: Response entity, response code
        """
        return HuxResponse.response(
            HTTPStatus.NOT_FOUND, message, None, None, extra_fields
        )

    @staticmethod
    def CONFLICT(
        message: str = None, extra_fields: dict = None
    ) -> Tuple[Response, int]:
        """Conflict (409)
        Args:
            message (str): Message to be returned.
            extra_fields (dict): dict containing any additional body parameters.
        Returns:
            Tuple[Response, int]: Response entity, response code
        """
        return HuxResponse.response(
            HTTPStatus.CONFLICT, message, None, None, extra_fields
        )

    @staticmethod
    def response(
        code: int,
        message: str = None,
        data: Union[dict, list] = None,
        data_schema: Schema = None,
        extra_fields: dict = None,
    ) -> Tuple[Response, int]:
        """Base response
        Args:
            code (int): Status code.
            message (str): Message to be returned.
            data (dict): Data to be returned.
            data_schema (Schema): Schema for the data.
            extra_fields (dict): dict containing any additional body parameters.
        Returns:
            Tuple[Response, int]: Response entity, response code
        """

        if message:
            body = {api_c.MESSAGE: message}
            if extra_fields:
                body = {**body, **extra_fields}

            return jsonify(body), code

        if data is not None:
            if not data_schema:
                return jsonify(data), code

            if isinstance(data, list):
                if not data:
                    return jsonify([]), code
                return jsonify(data_schema.dump(data, many=True)), code

            if isinstance(data, dict):
                return jsonify(data_schema.dump(data, many=False)), code

        return None
