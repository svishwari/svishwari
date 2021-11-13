"""Purpose of this file is for holding methods to query and pull data
from Tecton.
"""
import random
import time
from math import log10
import asyncio
from json import dumps
from typing import List, Tuple

from dateutil import parser
import aiohttp
import async_timeout
import requests
from huxunifylib.util.general.logging import logger

from huxunify.api.config import get_config
from huxunify.api.exceptions import integration_api_exceptions as iae
from huxunify.api import constants
from huxunify.api.schema.model import (
    ModelVersionSchema,
    FeatureSchema,
    ModelDriftSchema,
    ModelLiftSchema,
)
from huxunify.api.prometheus import (
    record_health_status_metric,
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
        record_health_status_metric(constants.TECTON_CONNECTION_HEALTH, True)
        return response.status_code, "Tecton available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        record_health_status_metric(constants.TECTON_CONNECTION_HEALTH, False)
        return False, getattr(exception, "message", repr(exception))


def map_model_response(response: dict) -> List[dict]:
    """Map model response to a usable dict.
    Args:
        response (dict): Input Tecton API response.

    Returns:
        List[dict]: A cleaned model dict.
    """

    models = []

    for meta_data in response.json()[constants.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[constants.FEATURES]
        model = {
            constants.ID: meta_data[constants.JOIN_KEYS][0],
            constants.LAST_TRAINED: parser.parse(feature[0]),
            constants.DESCRIPTION: feature[1],
            constants.FULCRUM_DATE: parser.parse(feature[2]),
            constants.LOOKBACK_WINDOW: int(feature[8]),
            constants.NAME: feature[4],
            constants.TYPE: str(feature[5]).lower(),
            constants.OWNER: feature[6],
            constants.STATUS: constants.MODEL_STATUS_MAPPING.get(
                feature[9], constants.STATUS_PENDING
            ),
            constants.LATEST_VERSION: feature[10],
            constants.PREDICTION_WINDOW: int(feature[3]),
            constants.PAST_VERSION_COUNT: 0,
        }
        models.append(model)

    return models


def map_model_version_history_response(
    response: dict, model_id: str
) -> List[dict]:
    """Map model version history response to a usable dict.

    Args:
        response (dict): Input Tecton API response.
        model_id (str): Model ID.

    Returns:
        List[dict]: A cleaned model version dict.
    """

    models = []

    for meta_data in response.json()[constants.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[constants.FEATURES]
        model = {
            constants.ID: model_id,
            constants.LAST_TRAINED: parser.parse(feature[0]),
            constants.DESCRIPTION: feature[1],
            constants.FULCRUM_DATE: parser.parse(feature[2]),
            constants.LOOKBACK_WINDOW: 7,
            constants.NAME: feature[5],
            constants.TYPE: str(feature[6]).lower(),
            constants.OWNER: feature[7],
            constants.STATUS: feature[9],
            constants.CURRENT_VERSION: meta_data[constants.JOIN_KEYS][0],
            constants.PREDICTION_WINDOW: int(feature[3]),
        }
        models.append(model)

    # sort the models based on the last trained date.
    models.sort(key=lambda x: x[constants.LAST_TRAINED], reverse=True)

    return models


def map_model_performance_response(
    response: dict,
    model_id: str,
    model_type: str,
    model_version: str,
    metric_default_value: float = -1,
) -> dict:
    """Map model performance response to a usable dict.

    Args:
        response (dict): Input Tecton API response.
        model_id (str): Model ID.
        model_type (str): Model type.
        model_version (str): Model version.
        metric_default_value: Default values for model metric.

    Returns:
        dict: A cleaned model performance dict.
    """

    if response.status_code != 200 or constants.RESULTS not in response.json():
        return {}

    for meta_data in response.json()[constants.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[constants.FEATURES]

        # get version based on model type and skip if not the provided version.
        if feature[4] != model_version:
            continue

        # grab the metrics based on model type and return.
        return {
            constants.ID: model_id,
            constants.RMSE: float(feature[0])
            if model_type in constants.REGRESSION_MODELS
            else metric_default_value,
            constants.AUC: float(feature[0])
            if model_type in constants.CLASSIFICATION_MODELS
            else metric_default_value,
            constants.PRECISION: float(feature[5])
            if model_type in constants.CLASSIFICATION_MODELS
            else metric_default_value,
            constants.RECALL: float(feature[6])
            if model_type in constants.CLASSIFICATION_MODELS
            else metric_default_value,
            constants.CURRENT_VERSION: model_version,
        }

    # nothing found, return an empty dict.
    return {}


def get_models() -> List[dict]:
    """Get models from Tecton.

    Args:

    Returns:
        List[dict]: List of models.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()

    # submit the post request to get the models
    response = requests.post(
        config.TECTON_FEATURE_SERVICE,
        dumps(constants.MODEL_LIST_PAYLOAD),
        headers=config.TECTON_API_HEADERS,
    )

    if response.status_code != 200 or constants.RESULTS not in response.json():
        logger.error(
            "Unable to retrieve models, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.TECTON_FEATURE_SERVICE} : in_function={get_models.__name__}",
            response.status_code,
        )

    return map_model_response(response)


def get_model_version_history(model_id: str) -> List[ModelVersionSchema]:
    """Get model version history based on id.

    Args:
        model_id (str): model id.

    Returns:
        List[ModelVersionSchema] List of model versions.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
        EmptyAPIResponseError: Response from integrated API call is empty.
    """

    # get config
    config = get_config()

    # payload
    payload = {
        "params": {
            "feature_service_name": constants.FEATURE_MODEL_HISTORY,
            "join_key_map": {"model_id": f"{model_id}"},
        }
    }

    response = requests.post(
        config.TECTON_FEATURE_SERVICE,
        dumps(payload),
        headers=config.TECTON_API_HEADERS,
    )

    if constants.RESULTS not in response.json():
        logger.error(
            "Unable to retrieve model version history, %s %s.",
            response.status_code,
            response.text,
        )
        if response.status_code == 200:
            raise iae.EmptyAPIResponseError(
                f"{config.TECTON_FEATURE_SERVICE} returned empty object",
                response.status_code,
            )
        raise iae.FailedAPIDependencyError(
            f"{config.TECTON_FEATURE_SERVICE} : in_function={get_model_version_history.__name__}",
            response.status_code,
        )

    # submit the post request to get the models
    return map_model_version_history_response(
        response,
        model_id,
    )


# pylint: disable=unused-argument
def get_model_drift(
    model_id: str, model_type: str, models: list
) -> List[ModelDriftSchema]:
    """Get model drift based on model_id and model_type.

    Args:
        model_id (str): Model id.
        model_type (str): model type.
        models (list): list of model versions.

    Returns:
        List[DriftSchema] List of model drift.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
        EmptyAPIResponseError: Response from integrated API call is empty.
    """

    # get config
    config = get_config()

    if model_type in constants.CLASSIFICATION_MODELS:
        service_name = constants.FEATURE_DRIFT_CLASSIFICATION_MODEL_SERVICE
    else:
        service_name = constants.FEATURE_DRIFT_REGRESSION_MODEL_SERVICE

    # payload
    payload = {
        "params": {
            "feature_service_name": service_name,
            "join_key_map": {constants.MODEL_ID: f"{model_id}"},
        }
    }

    # start timer
    timer = time.perf_counter()

    response = requests.post(
        config.TECTON_FEATURE_SERVICE,
        dumps(payload),
        headers=config.TECTON_API_HEADERS,
    )

    # log execution time summary
    total_ticks = time.perf_counter() - timer
    logger.info(
        "Executed drift chart data request to the Tecton API in %0.4f seconds.",
        total_ticks,
    )

    if constants.RESULTS not in response.json():
        logger.error(
            "Unable to retrieve model drift, %s %s.",
            response.status_code,
            response.text,
        )
        if response.status_code == 200:
            raise iae.EmptyAPIResponseError(
                f"{config.TECTON_FEATURE_SERVICE} returned empty object",
                response.status_code,
            )
        raise iae.FailedAPIDependencyError(
            f"{config.TECTON_FEATURE_SERVICE} : in_function={get_model_drift.__name__}",
            response.status_code,
        )

    result_drift = []
    for result in response.json().get(constants.RESULTS, []):
        if not result:
            continue

        # look up run date from model version
        run_dates = [
            m[constants.LAST_TRAINED]
            for m in models
            if m[constants.CURRENT_VERSION] == result[constants.FEATURES][4]
        ]

        result_drift.append(
            {
                # check if model version matched, otherwise parse the created date.
                constants.RUN_DATE: run_dates[0]
                if run_dates
                else parser.parse(result[constants.FEATURES][1]),
                constants.DRIFT: result[constants.FEATURES][0],
            }
        )

    # sort the results by time
    if result_drift:
        result_drift.sort(key=lambda x: x[constants.RUN_DATE])

    return result_drift


def get_model_lift_async(model_id: str) -> List[ModelLiftSchema]:
    """Get model lift based on id.

    Args:
        model_id (str): model id.

    Returns:
         List[ModelLiftSchema]: List of model lift.
    """

    # set the event loop
    asyncio.set_event_loop(asyncio.SelectorEventLoop())

    # start timer
    timer = time.perf_counter()

    # send all responses at once and wait until they are all done.
    responses = asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            *(
                get_async_lift_bucket(model_id, bucket)
                for bucket in range(10, 101, 10)
            )
        )
    )

    # log execution time summary
    total_ticks = time.perf_counter() - timer
    logger.info(
        "Executed 10 requests to the Tecton API in %0.4f seconds. ~%0.4f requests per second.",
        total_ticks,
        total_ticks / 10,
    )

    result_lift = []
    # iterate each response.
    for response in responses:
        # validate response code
        if not response[0]:
            continue

        # process lift data
        latest_lift_data = response[0][constants.RESULTS][-1][
            constants.FEATURES
        ]

        result_lift.append(
            {
                constants.BUCKET: response[1],
                constants.ACTUAL_VALUE: latest_lift_data[0],
                constants.ACTUAL_LIFT: latest_lift_data[2],
                constants.PREDICTED_LIFT: latest_lift_data[3],
                constants.PREDICTED_VALUE: latest_lift_data[8],
                constants.PROFILE_COUNT: int(latest_lift_data[9]),
                constants.ACTUAL_RATE: latest_lift_data[10],
                constants.PREDICTED_RATE: latest_lift_data[11],
                constants.PROFILE_SIZE_PERCENT: latest_lift_data[13] * 100
                if latest_lift_data[13]
                else 0,
            }
        )

    return result_lift


async def get_async_lift_bucket(
    model_id: str, bucket: int
) -> Tuple[dict, int]:
    """Asynchronously gets lift by bucket.

    Args:
        model_id (str): model id.
        bucket (int): bucket.

    Returns:
       Tuple[dict,int]: bucket lift dict.
    """

    # get config
    config = get_config()

    payload = {
        "params": {
            "feature_service_name": constants.FEATURE_LIFT_MODEL_SERVICE,
            "join_key_map": {
                constants.MODEL_ID: str(model_id),
                constants.BUCKET: str(bucket),
            },
        }
    }

    # setup the aiohttp session so we can process the calls asynchronously
    async with aiohttp.ClientSession() as session, async_timeout.timeout(10):
        # run the async post request
        async with session.post(
            config.TECTON_FEATURE_SERVICE,
            json=payload,
            headers=config.TECTON_API_HEADERS,
        ) as response:
            # await the responses, and return them as they come in.
            try:
                return await response.json(), bucket
            except aiohttp.client.ContentTypeError:
                logger.error(
                    "Tecton post request failed for bucket: %s.", bucket
                )
                return {"code": 500}, bucket


def get_model_features(
    model_id: str, model_version: str
) -> List[FeatureSchema]:
    """Get model features based on model id.

    Args:
        model_id (str): Model id.
        model_version (str): model version.

    Returns:
        List[FeatureSchema]: List of model features.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()

    # Tecton forces us to get the feature at the version level, so we have to
    # query the service in succession. We break on the first empty value.
    result_features = []
    for i in range(200):
        payload = {
            "params": {
                "feature_service_name": constants.FEATURE_TOP_SERVICE,
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
                    constants.STATUS: constants.STATUS_ACTIVE,
                    constants.POPULARITY: random.randint(1, 3),
                    constants.SCORE: round(
                        log10(float(feature[2]))
                        if float(feature[2]) > 0
                        else -log10(float(abs(feature[2]))),
                        4,
                    ),
                }
            )

    if not result_features:
        logger.error(
            "Unable to retrieve model features, %s %s.",
            response.status_code,
            response.text,
        )

    return result_features


def get_model_performance_metrics(
    model_id: str, model_type: str, model_version: str
) -> dict:
    """Get model performance metrics based on model ID.

    Args:
        model_id (str): Model id.
        model_type (str): Model type.
        model_version (str): Model version.

    Returns:
         dict: Model performance metrics.
    """

    # get config
    config = get_config()

    # regression models calculate RMSE
    if model_type in constants.REGRESSION_MODELS:
        service_name = constants.FEATURE_DRIFT_REGRESSION_MODEL_SERVICE
    # classification models calculate AUC, Precision, Recall
    elif model_type in constants.CLASSIFICATION_MODELS:
        service_name = constants.FEATURE_DRIFT_CLASSIFICATION_MODEL_SERVICE
    else:
        logger.warning("Model type not supported '%s'.", model_type)

    # set payload and service name.
    payload = {
        "params": {
            "feature_service_name": service_name,
            "join_key_map": {"model_id": f"{model_id}"},
        }
    }

    logger.info("Querying Tecton for model performance metrics.")
    response = requests.post(
        config.TECTON_FEATURE_SERVICE,
        dumps(payload),
        headers=config.TECTON_API_HEADERS,
    )
    logger.info("Querying Tecton for model performance metrics complete.")

    # submit the post request to get the model metrics.
    return map_model_performance_response(
        response,
        model_id,
        model_type,
        model_version,
    )
