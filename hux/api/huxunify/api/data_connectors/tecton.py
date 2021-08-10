"""
Purpose of this file is for holding methods to query and pull data from Tecton.
"""
from json import dumps
from typing import List, Tuple

from dateutil import parser
import requests

from huxunify.api.config import get_config
from huxunify.api import constants
from huxunify.api.schema.model import (
    ModelVersionSchema,
    FeatureImportance,
    FeatureSchema,
    DriftSchema,
    LiftSchema,
    PerformanceMetricSchema,
)


def check_tecton_connection() -> Tuple[bool, str]:
    """Validate the tecton connection.
    Args:

    Returns:
        tuple[bool, str]: Returns if the connection is valid, and the message.
    """
    # get config
    config = get_config()

    # submit the post request to get models
    try:
        response = requests.post(
            config.TECTON_FEATURE_SERVICE,
            dumps(constants.MODEL_LIST_PAYLOAD),
            headers=config.TECTON_API_HEADERS,
        )
        return response.status_code, "Tecton available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        return False, getattr(exception, "message", repr(exception))


def map_model_response(response: dict) -> List[dict]:
    """Map model response to a usable dict.
    Args:
        response (dict): Input Tecton API response.

    Returns:
        List[dict]: A cleaned model dict.

    """
    if response.status_code != 200:
        return []

    if constants.RESULTS not in response.json():
        return []

    models = []
    for meta_data in response.json()[constants.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[constants.FEATURES]
        model = {
            constants.ID: meta_data[constants.JOIN_KEYS][0],
            constants.LAST_TRAINED: parser.parse(feature[0]),
            constants.DESCRIPTION: feature[1],
            constants.FULCRUM_DATE: parser.parse(feature[2]),
            constants.LOOKBACK_WINDOW: int(feature[3]),
            constants.NAME: feature[4],
            constants.TYPE: feature[5],
            constants.OWNER: feature[6],
            constants.STATUS: feature[8],
            constants.LATEST_VERSION: feature[9],
            constants.PREDICTION_WINDOW: int(feature[3]),
            constants.PAST_VERSION_COUNT: 0,
        }
        models.append(model)
    return models


def map_model_version_history_response(
    response: dict, model_id: int
) -> List[dict]:
    """Map model version history response to a usable dict.
    Args:
        response (dict): Input Tecton API response.
        model_id (int): Model ID number.

    Returns:
        List[dict]: A cleaned model version dict.

    """
    if response.status_code != 200:
        return []

    if constants.RESULTS not in response.json():
        return []

    models = []

    for meta_data in response.json()[constants.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[constants.FEATURES]
        model = {
            constants.ID: model_id,
            constants.LAST_TRAINED: parser.parse(feature[0]),
            constants.DESCRIPTION: feature[1],
            constants.FULCRUM_DATE: parser.parse(feature[2]),
            constants.LOOKBACK_WINDOW: int(feature[3]),
            constants.NAME: feature[5],
            constants.TYPE: feature[5],
            constants.OWNER: feature[7],
            constants.STATUS: feature[9],
            constants.CURRENT_VERSION: meta_data[constants.JOIN_KEYS][0],
            constants.PREDICTION_WINDOW: int(feature[3]),
        }
        models.append(model)
    return models


def get_models() -> List[dict]:
    """Get models from Tecton.

    Args:

    Returns:
        List[dict]: List of models.
    """

    # get config
    config = get_config()

    # submit the post request to get the models
    response = requests.post(
        config.TECTON_FEATURE_SERVICE,
        dumps(constants.MODEL_LIST_PAYLOAD),
        headers=config.TECTON_API_HEADERS,
    )
    return map_model_response(response)


# pylint: disable=unused-argument
def get_model_version_history(model_id: int) -> List[ModelVersionSchema]:
    """Get model version history based on name.

    Args:
        model_id (int): model name.

    Returns:
         List[ModelVersionSchema] List of model versions.
    """
    # get config
    config = get_config()

    # payload
    payload = {
        "params": {
            "feature_service_name": "ui_metadata_model_history_service",
            "join_key_map": {"model_id": f"{model_id}"},
        }
    }

    # submit the post request to get the models
    response = requests.post(
        config.TECTON_FEATURE_SERVICE,
        dumps(payload),
        headers=config.TECTON_API_HEADERS,
    )
    return map_model_version_history_response(response, model_id)


# pylint: disable=unused-argument
def get_model_drift(name: str) -> List[DriftSchema]:
    """Get model drift based on name.

    Args:
        name (str): model name.

    Returns:
         List[DriftSchema] List of model drift.
    """
    # TODO - when available.
    return []


# pylint: disable=unused-argument
def get_model_lift(name: str) -> List[LiftSchema]:
    """Get model lift based on name.

    Args:
        name (str): model name.

    Returns:
         List[LiftSchema] List of model lift.
    """
    # TODO - when available.
    return []


# pylint: disable=unused-argument
def get_model_feature_importance(name: str) -> List[FeatureImportance]:
    """Get model feature importance based on name.

    Args:
        name (str): model name.

    Returns:
         List[FeatureImportance] List of model feature importance.
    """
    # TODO - when available.
    return []


# pylint: disable=unused-argument
def get_model_features(name: str) -> List[FeatureSchema]:
    """Get model features based on name.

    Args:
        name (str): model name.

    Returns:
         List[FeatureSchema] List of model features.
    """
    # TODO - when available.
    return []


# pylint: disable=unused-argument
def get_model_performance_metrics(name: str) -> List[PerformanceMetricSchema]:
    """Get model performance metrics based on name.

    Args:
        name (str): model name.

    Returns:
         List[PerformanceMetricSchema] List of model performance metrics.
    """
    # TODO - when available.
    return []
