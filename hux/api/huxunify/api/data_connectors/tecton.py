"""
Purpose of this file is for holding methods to query and pull data from Tecton.
"""
import difflib
import random
from math import log10
from json import dumps
from typing import List, Tuple

from dateutil import parser
import requests

from huxunify.api.config import get_config
from huxunify.api import constants
from huxunify.api.schema.model import (
    ModelVersionSchema,
    FeatureSchema,
    DriftSchema,
    LiftSchema,
    PerformanceMetricSchema,
)


def get_model_type(
    model_name: str, default_type: str = constants.UNKNOWN
) -> str:
    """Get the model type based on keywords.

    Args:
        model_name (str): Name of the model.
        default_type (str): Default type of model if no mapping found.

    Returns:
         str: Model type.
    """

    # get the closest match, otherwise return the default
    matches = difflib.get_close_matches(
        model_name.lower(), constants.MODEL_TYPES
    )
    return matches[0] if matches else default_type


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
            constants.TYPE: get_model_type(feature[5]),
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
            constants.TYPE: get_model_type(feature[5]),
            constants.OWNER: feature[7],
            constants.STATUS: feature[9],
            constants.CURRENT_VERSION: meta_data[constants.JOIN_KEYS][0],
            constants.PREDICTION_WINDOW: int(feature[3]),
        }
        models.append(model)
    return models


def map_model_performance_response(
    response: dict, model_id: int, model_type: str, model_version: str
) -> List[dict]:
    """Map model performance response to a usable dict.

    Args:
        response (dict): Input Tecton API response.
        model_id (int): Model ID number.

    Returns:
        List[dict]: A cleaned model performance dict.

    """
    if response.status_code != 200:
        return []

    if constants.RESULTS not in response.json():
        return []

    models = []

    for meta_data in response.json()[constants.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[constants.FEATURES]

        # skip if not the provided version.
        if feature[4] != model_version:
            continue

        models.append(
            {
                constants.ID: model_id,
                constants.RMSE: float(feature[0])
                if model_type in constants.REGRESSION_MODELS
                else 0,
                constants.AUC: float(feature[0])
                if model_type in constants.CLASSIFICATION_MODELS
                else 0,
                constants.PRECISION: float(feature[5])
                if model_type in constants.CLASSIFICATION_MODELS
                else 0,
                constants.RECALL: float(feature[6])
                if model_type in constants.CLASSIFICATION_MODELS
                else 0,
                constants.CURRENT_VERSION: model_version,
            }
        )
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


def get_model_version_history(model_id: int) -> List[ModelVersionSchema]:
    """Get model version history based on id.

    Args:
        model_id (int): model id.

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
    return map_model_version_history_response(
        requests.post(
            config.TECTON_FEATURE_SERVICE,
            dumps(payload),
            headers=config.TECTON_API_HEADERS,
        ),
        model_id,
    )


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


def get_model_features(
    model_id: int, model_version: str
) -> List[FeatureSchema]:
    """Get model features based on model id.

    Args:
        model_id (int): model id.
        model_version (str): model version.

    Returns:
         List[FeatureSchema] List of model features.
    """

    # get config
    config = get_config()

    # Tecton forces us to get the feature at the version level, so we have to
    # query the service in succession. We break on the first empty value.
    result_features = []
    for i in range(200):
        payload = {
            "params": {
                "feature_service_name": "ui_metadata_model_top_features_service",
                "join_key_map": {"model_id": f"{model_id}", "rank": str(i)},
            }
        }

        response = requests.post(
            config.TECTON_FEATURE_SERVICE,
            dumps(payload),
            headers=config.TECTON_API_HEADERS,
        )

        if response.status_code != 200:
            break

        if constants.RESULTS not in response.json():
            break

        # grab the features and match model version.
        features = [
            x[constants.FEATURES]
            for x in response.json()[constants.RESULTS]
            if x["joinKeys"][0] == model_version
        ]
        for feature in features:
            # TODO - HUS-910, remove the random string values below once Tecton is returning them.
            result_features.append(
                {
                    constants.ID: model_id,
                    constants.VERSION: model_version,
                    constants.NAME: feature[1],
                    constants.FEATURE_SERVICE: feature[4],
                    constants.DATA_SOURCE: random.choice(
                        ["Buyers", "Retail", "Promotion", "Email", "Ecommerce"]
                    ),
                    constants.CREATED_BY: random.choice(
                        ["Susan Miller", "Jack Miller"]
                    ),
                    constants.STATUS: random.choice(
                        [
                            constants.STATUS_PENDING,
                            constants.STATUS_ACTIVE,
                            constants.STATUS_STOPPED,
                        ]
                    ),
                    constants.POPULARITY: random.randint(1, 3),
                    constants.SCORE: round(log10(float(feature[2])), 4),
                }
            )

    # submit the post request to get the models
    return result_features


# pylint: disable=unused-argument
def get_model_performance_metrics(
    model_id: id, model_type: str, model_version: str
) -> List[PerformanceMetricSchema]:
    """Get model performance metrics based on model ID.

    Args:
        model_id (int): Model id.
        model_type (str): Model type.

    Returns:
         List[PerformanceMetricSchema] List of model performance metrics.
    """

    # get config
    config = get_config()

    # regression models calculate RMSE
    if model_type in constants.REGRESSION_MODELS:
        service_name = "ui_metadata_model_metrics_regression_service"
    # classification models calculate AUC, Precision, Recall
    elif model_type in constants.CLASSIFICATION_MODELS:
        service_name = "ui_metadata_model_metrics_classification_service"
    else:
        raise ValueError(f"Model type not supported {model_type}")

    # payload
    payload = {
        "params": {
            "feature_service_name": service_name,
            "join_key_map": {"model_id": f"{model_id}"},
        }
    }

    # submit the post request to get the models
    return map_model_performance_response(
        requests.post(
            config.TECTON_FEATURE_SERVICE,
            dumps(payload),
            headers=config.TECTON_API_HEADERS,
        ),
        model_id,
        model_type,
        model_version,
    )
