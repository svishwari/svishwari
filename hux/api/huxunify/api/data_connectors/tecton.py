"""
Purpose of this file is for holding methods to query and pull data from Tecton.
"""
from json import dumps
from typing import List

import requests

from huxunify.api import config
from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    FeatureImportance,
    FeatureSchema,
    DriftSchema,
    LiftSchema,
    PerformanceMetricSchema,
)


# pylint: disable=unused-argument
def get_models() -> List[ModelSchema]:
    """Get models from Tecton.
    Args:

    Returns:
        List[ModelSchema]: List of models.
    """
    # setup the payload
    payload = dumps(
        {
            "params": {
                "feature_service_name": "ui_metadata_models_service",
                "join_key_map": {
                    "model_name": "ltv-model-365-30",
                    "version_number": "0.0.1",
                },
            }
        }
    )

    # submit the post request to get the models
    return requests.post(
        config.TECTON_FEATURE_SERVICE,
        payload,
        headers=config.TECTON_API_HEADERS,
    ).json()


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
         List[PerformanceMetricSchema] List of model lift.
    """
    # TODO - when available.
    return []
