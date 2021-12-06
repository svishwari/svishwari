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

from huxunify.api import constants as api_c
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
            dumps(api_c.MODEL_LIST_PAYLOAD),
            headers=config.TECTON_API_HEADERS,
        )

        record_health_status_metric(api_c.TECTON_CONNECTION_HEALTH, response.status_code == 200)
        if response.status_code == 200:
            return True, "Tecton available."
        else:
            return False, f"Tecton not available. Received: {response.status_code}"

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        record_health_status_metric(api_c.TECTON_CONNECTION_HEALTH, False)
        return False, getattr(exception, "message", repr(exception))


def map_model_response(response: dict) -> List[dict]:
    """Map model response to a usable dict.
    Args:
        response (dict): Input Tecton API response.

    Returns:
        List[dict]: A cleaned model dict.
    """

    models = []

    for meta_data in response.json()[api_c.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[api_c.FEATURES]
        model = {
            api_c.ID: meta_data[api_c.JOIN_KEYS][0],
            api_c.LAST_TRAINED: parser.parse(feature[0]),
            api_c.DESCRIPTION: feature[1],
            api_c.FULCRUM_DATE: parser.parse(feature[2]),
            api_c.LOOKBACK_WINDOW: int(feature[8]),
            api_c.NAME: feature[4],
            api_c.TYPE: str(feature[5]).lower(),
            api_c.OWNER: feature[6],
            api_c.STATUS: api_c.MODEL_STATUS_MAPPING.get(
                feature[9], api_c.STATUS_PENDING
            ),
            api_c.LATEST_VERSION: feature[10],
            api_c.PREDICTION_WINDOW: int(feature[3]),
            api_c.PAST_VERSION_COUNT: 0,
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

    for meta_data in response.json()[api_c.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[api_c.FEATURES]
        model = {
            api_c.ID: model_id,
            api_c.LAST_TRAINED: parser.parse(feature[0]),
            api_c.DESCRIPTION: feature[1],
            api_c.FULCRUM_DATE: parser.parse(feature[2]),
            api_c.LOOKBACK_WINDOW: 7,
            api_c.NAME: feature[5],
            api_c.TYPE: str(feature[6]).lower(),
            api_c.OWNER: feature[7],
            api_c.STATUS: feature[9],
            api_c.CURRENT_VERSION: meta_data[api_c.JOIN_KEYS][0],
            api_c.PREDICTION_WINDOW: int(feature[3]),
        }
        models.append(model)

    # sort the models based on the last trained date.
    models.sort(key=lambda x: x[api_c.LAST_TRAINED], reverse=True)

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

    if response.status_code != 200 or api_c.RESULTS not in response.json():
        return {}

    for meta_data in response.json()[api_c.RESULTS]:
        # get model metadata from tecton
        feature = meta_data[api_c.FEATURES]

        # get version based on model type and skip if not the provided version.
        if feature[4] != model_version:
            continue

        # grab the metrics based on model type and return.
        return {
            api_c.ID: model_id,
            api_c.RMSE: float(feature[0])
            if model_type in api_c.REGRESSION_MODELS
            else metric_default_value,
            api_c.AUC: float(feature[0])
            if model_type in api_c.CLASSIFICATION_MODELS
            else metric_default_value,
            api_c.PRECISION: float(feature[5])
            if model_type in api_c.CLASSIFICATION_MODELS
            else metric_default_value,
            api_c.RECALL: float(feature[6])
            if model_type in api_c.CLASSIFICATION_MODELS
            else metric_default_value,
            api_c.CURRENT_VERSION: model_version,
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
        dumps(api_c.MODEL_LIST_PAYLOAD),
        headers=config.TECTON_API_HEADERS,
    )

    if response.status_code != 200 or api_c.RESULTS not in response.json():
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
            "feature_service_name": api_c.FEATURE_MODEL_HISTORY,
            "join_key_map": {"model_id": f"{model_id}"},
        }
    }

    response = requests.post(
        config.TECTON_FEATURE_SERVICE,
        dumps(payload),
        headers=config.TECTON_API_HEADERS,
    )

    if api_c.RESULTS not in response.json():
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

    if model_type in api_c.CLASSIFICATION_MODELS:
        service_name = api_c.FEATURE_DRIFT_CLASSIFICATION_MODEL_SERVICE
    else:
        service_name = api_c.FEATURE_DRIFT_REGRESSION_MODEL_SERVICE

    # payload
    payload = {
        "params": {
            "feature_service_name": service_name,
            "join_key_map": {api_c.MODEL_ID: f"{model_id}"},
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

    if api_c.RESULTS not in response.json():
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
    for result in response.json().get(api_c.RESULTS, []):
        if not result:
            continue

        # look up run date from model version
        run_dates = [
            m[api_c.LAST_TRAINED]
            for m in models
            if m[api_c.CURRENT_VERSION] == result[api_c.FEATURES][4]
        ]

        result_drift.append(
            {
                # check if model version matched, otherwise parse the created date.
                api_c.RUN_DATE: run_dates[0]
                if run_dates
                else parser.parse(result[api_c.FEATURES][1]),
                api_c.DRIFT: result[api_c.FEATURES][0],
            }
        )

    # sort the results by time
    if result_drift:
        result_drift.sort(key=lambda x: x[api_c.RUN_DATE])

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
        latest_lift_data = response[0][api_c.RESULTS][-1][api_c.FEATURES]

        result_lift.append(
            {
                api_c.BUCKET: response[1],
                api_c.ACTUAL_VALUE: latest_lift_data[0],
                api_c.ACTUAL_LIFT: latest_lift_data[2],
                api_c.PREDICTED_LIFT: latest_lift_data[3],
                api_c.PREDICTED_VALUE: latest_lift_data[8],
                api_c.PROFILE_COUNT: int(latest_lift_data[9]),
                api_c.ACTUAL_RATE: latest_lift_data[10],
                api_c.PREDICTED_RATE: latest_lift_data[11],
                api_c.PROFILE_SIZE_PERCENT: latest_lift_data[13] * 100
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
            "feature_service_name": api_c.FEATURE_LIFT_MODEL_SERVICE,
            "join_key_map": {
                api_c.MODEL_ID: str(model_id),
                api_c.BUCKET: str(bucket),
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
                "feature_service_name": api_c.FEATURE_TOP_SERVICE,
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

        if api_c.RESULTS not in response.json():
            break

        # grab the features and match model version.
        features = [
            x[api_c.FEATURES]
            for x in response.json()[api_c.RESULTS]
            if x["joinKeys"][0] == model_version
        ]

        # check if any features available for the first bucket,
        # if not it means there are none for that version.
        if not features:
            break

        for feature in features:
            # get score.
            score = 0
            try:
                score = (
                    log10(float(feature[2]))
                    if float(feature[2]) > 0
                    else -log10(float(abs(feature[2])))
                )
            except ValueError:
                pass

            # TODO - HUS-910, remove the random string values below once Tecton is returning them.
            result_features.append(
                {
                    api_c.ID: model_id,
                    api_c.VERSION: model_version,
                    api_c.NAME: feature[1],
                    api_c.FEATURE_SERVICE: feature[4],
                    api_c.DATA_SOURCE: random.choice(
                        ["Buyers", "Retail", "Promotion", "Email", "Ecommerce"]
                    ),
                    api_c.CREATED_BY: random.choice(
                        ["Susan Miller", "Jack Miller"]
                    ),
                    api_c.STATUS: api_c.STATUS_ACTIVE,
                    api_c.POPULARITY: random.randint(1, 3),
                    api_c.SCORE: round(score, 4),
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
    if model_type in api_c.REGRESSION_MODELS:
        service_name = api_c.FEATURE_DRIFT_REGRESSION_MODEL_SERVICE
    # classification models calculate AUC, Precision, Recall
    elif model_type in api_c.CLASSIFICATION_MODELS:
        service_name = api_c.FEATURE_DRIFT_CLASSIFICATION_MODEL_SERVICE
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
