"""
Purpose of this file is for holding methods to query and pull data from Tecton.
"""
from json import dumps
from typing import List, Tuple

import dateutil.parser as parser
import requests

from huxunify.api import config
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
    # submit the post request to get models
    response = requests.post(
        config.TECTON_FEATURE_SERVICE,
        dumps(constants.MODEL_LIST_PAYLOAD),
        headers=config.TECTON_API_HEADERS,
    )
    return response.status_code == 200, response.reason


def map_model_response(response: dict) -> dict:
    """Map model response to a usable dict.
    Args:
        response (dict): Input Tecton API response.

    Returns:
        dict: A cleaned model dict.

    """
    if response.status_code != 200:
        return []

    if constants.RESULTS not in response.json():
        return []

    models = []
    for meta_data in response.json()[constants.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[constants.FEATURES]
        version = meta_data[constants.JOIN_KEYS][0]
        model = {
            constants.ID: 1,
            constants.LATEST_VERSION: version,
            constants.FULCRUM_DATE: parser.parse(feature[0]),
            constants.DESCRIPTION: feature[1],
            constants.LAST_TRAINED: parser.parse(feature[2]),
            constants.LOOKBACK_WINDOW: feature[3],
            constants.NAME: feature[4],
            constants.OWNER: feature[5],
            constants.PREDICTION_WINDOW: int(feature[4].split("-")[-1]),
            constants.STATUS: feature[7],
            constants.TYPE: feature[4].split("-")[0],
        }
        models.append(model)

    # sort by version number
    models = sorted(
        models, key=lambda k: k[constants.LATEST_VERSION], reverse=True
    )

    # take first model
    model = models[0]

    # assign version count
    model[constants.PAST_VERSION_COUNT] = (
        sum([1 for x in models if x[constants.NAME] == model[constants.NAME]])
        - 1
    )

    return model


def get_models(model_ids: list = None) -> List[dict]:
    """Get models from Tecton.
    Args:
        model_ids (list): List of model ids to query.

    Returns:
        List[ModelSchema]: List of models.
    """

    if model_ids is None:
        # TODO - update when tecton makes the list available to get.
        model_ids = [1]

    # submit the post request to get the models
    models = []
    for model_id in model_ids:
        # grab the payload and filter by ID
        model_payload = constants.MODEL_LIST_PAYLOAD

        # specific to this model.
        model_payload["params"]["join_key_map"]["model_id"] = str(model_id)

        response = requests.post(
            config.TECTON_FEATURE_SERVICE,
            dumps(model_payload),
            headers=config.TECTON_API_HEADERS,
        )
        mapped_model = map_model_response(response)
        if not mapped_model:
            continue

        models.append(mapped_model)

    return models


# pylint: disable=unused-argument
def get_model_version_history(name: str) -> List[ModelVersionSchema]:
    """Get model version history based on name.

    Args:
        name (str): model name.

    Returns:
         List[ModelVersionSchema] List of model versions.
    """
    # TODO - when available.
    return []


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
