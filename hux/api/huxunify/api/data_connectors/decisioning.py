import json
from pprint import pprint
from datetime import datetime

import requests
from huxmodelclient import api_client, configuration
from huxmodelclient.api import DefaultApi as dec_client
from huxunify.api.config import get_config


token = "eyJraWQiOiJoTjFIeDl6ZGVyZWVDbmRlU2dfWGZjRzJtZDhIZGFVYUk4MkRKRFltV0dZIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIwMHVhNjB6ZjFpMm1OakhzSzJwNyIsIm5hbWUiOiJKaW0gTWNNYWhvbiIsImVtYWlsIjoiamltY21haG9uQGRlbG9pdHRlLmNvbSIsInZlciI6MSwiaXNzIjoiaHR0cHM6Ly9kZWxvaXR0ZWRpZ2l0YWwtbXMub2t0YS5jb20iLCJhdWQiOiIwb2FiZWxjMGh5Z3BteDRPVDJwNyIsImlhdCI6MTY1MTQ2MDYyMywiZXhwIjoxNjUxNDY0MjIzLCJqdGkiOiJJRC5nSWtCRHlBQlRha1dCTnphb2NmY3JDR3lrSTdvdW9FS2hnTFlWa0pGSmVrIiwiYW1yIjpbIm90cCIsInB3ZCIsIm1mYSJdLCJpZHAiOiIwb2FmZHVzNGhyM01pRGZ0QjJwNiIsIm5vbmNlIjoiNmFUZ3VlSGdkM1V3T2l4U3pQQUs5WUNHVVdhSDlUUVU3anlqTkZ4RUpldmFrVUF5U1ZaNnFTREQxdnd5VElzNyIsInByZWZlcnJlZF91c2VybmFtZSI6ImppbWNtYWhvbkBkZWxvaXR0ZS5jb20iLCJhdXRoX3RpbWUiOjE2NTE0NjA1NDksImF0X2hhc2giOiJOSHMyak53SmxRWW53bklreVRQbHhBIn0.LGcQsNl2z_j9VC_sLK-ib9TRmFiwfIw7MczsqAH5DeqV6W_QwUerHQfsISDsV4UM7-VhXh73NL5Omw1XsxVmbsUC6BHbmjfAE2M0fHMa6hHc5QW7XZLC8I7HagJyqemoXl48UC5dseSDqf6XwqQB35wQ_qdPEw9vgBXmbAal-nbH_8RxscgA3d3APbSvkG4o3C9De5_PmDmNXZFWrek67MuwuJE9RuJOdM2HOdRMeinPyy5ShCExW7-BCtTkGk0SXn6rrj6LRsbwB28JrRRScoXxYrRqANq0qSYR2MDnlCzJdpfB-cYFt4Nw6OND43fNcD-mYO-HqyoJrZSWdzGsUg"


def dec_call(url: str):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url=url, headers=headers).json()


class Decisioning:
    def __init__(self, token: str):
        self.token = token
        config = configuration.Configuration(
            host="https://hux-model-api-dec.decisioning-pendleton.in",
        )
        # config = configuration.Configuration(get_config().DECISIONING_URL)
        self.decisioning_client = dec_client(
            api_client=api_client.ApiClient(configuration=config)
        )

    def get_all_model_ids(self) -> list:
        """Gets a list of all models from decisioning.

        Returns:
            list: list of model names.
        """
        # resp = dec_call(
        #     "https://hux-model-api-dec.decisioning-pendleton.in/api/v1alpha1/models"
        # )
        # return [model["model_id"] for model in resp]
        # # return dec_call("https://hux-model-api-dec.decisioning-pendleton.in/api/v1alpha1/models")
        return self.decisioning_client.get_models_api_v1alpha1_models_get()

    def get_model_info(self, model_id: str) -> dict:
        """Gets the current info for a model from decisioning.

        Args:
            model_id (str): ID of the model.

        Returns:
            dict: model info dictionary.
        """
        model_infos = dec_call(
            f"https://hux-model-api-dec.decisioning-pendleton.in/api/v1alpha1/models/{model_id}"
        )
        current_info = max(
            model_infos,
            key=lambda info: datetime.strptime(
                info["scheduled_date"], "%Y-%m-%d"
            ),
        )
        current_info["past_version_count"] = len(model_infos)
        return current_info
        # return self.decisioning_client.get_model_info_api_v1alpha1_models_model_id_get(
        #     model_id
        # )[
        #     0
        # ].to_dict()

    def get_model_info_history(self, model_id: str) -> list:
        """Gets current and previous info objects for a model from decisioning.

        Args:
            model_id (str): ID of the model.

        Returns:
            list: list of model info.
        """
        return dec_call(
            f"https://hux-model-api-dec.decisioning-pendleton.in/api/v1alpha1/models/{model_id}"
        )

    def get_health_status(self):
        """ Get the health status of the Decisioning API

        Returns:

        """

        return self.decisioning_client.healthz_api_v1alpha1_healthz_get()

    def get_all_models(self) -> list:
        """Gets a list of all models

        Returns:
            list: list of all models
        """
        models = []
        model_ids = self.get_all_model_ids()

        for model_id in model_ids:
            model_info = self.get_model_info(model_id)

            models.append(
                {
                    "id": model_info["model_id"],
                    "name": model_info["model_metadata"]["model_name"],
                    "description": model_info["model_metadata"]["description"],
                    "status": model_info["model_metadata"]["status"].lower(),
                    "latest_version": model_info["model_version"],
                    "owner": model_info["model_metadata"]["owner"],
                    "lookback_window": model_info["model_metadata"][
                        "lookback_days"
                    ],
                    "prediction_window": model_info["model_metadata"][
                        "prediction_days"
                    ],
                    "fulcrum_date": model_info["model_metadata"][
                        "fulcrum_date"
                    ],
                    "last_trained": model_info["scheduled_date"],
                    "type": model_info["model_metadata"]["model_type"],
                    "category": model_info["model_metadata"]["model_type"].lower(),
                    "past_version_count": model_info["past_version_count"],
                    "is_enabled": True,
                    "is_added": True,
                }
            )

        return models

    # TODO test
    def get_model_overview(self, model_id: str) -> dict:
        """Get the feature importance for a model

        Args:
            model_id (str): ID of the model.

        Returns:
            list: feature importance statistics for the model.
        """
        model_info = self.get_model_info(model_id)
        rmse = model_info["model_metrics"]["rmse"]

        return {
            "model_type": model_info["model_metadata"]["model_type"],
            "model_name": model_info["model_metadata"]["model_name"],
            "description": model_info["model_metadata"]["description"],
            "performance_metric": {
                "rmse": rmse if rmse else -1.0,
                "auc": model_info["model_metrics"]["AUC"],
                "precision": model_info["model_metrics"]["precision"],
                "recall": model_info["model_metrics"]["recall"],
                "current_version": model_info["model_version"],
            }
        }

    # TODO pick which data, test
    def get_model_features(self, model_id: str) -> list:
        """Get the features for a model

        Args:
            model_id (str): ID of the model.

        Returns:
            list: feature statistics for the model.
        """
        features = []
        model_info = self.get_model_info(model_id)

        for feature in model_info["important_features"]:
            features.append(
                {
                    "id": feature["model_id"],
                    "name": feature["model_name"],
                    "description": feature["model_description"],
                    "feature_type": feature["model_type"],
                    "records_not_null": "-",
                    "feature_importance": "-",
                    "mean": "-",
                    "min": "-",
                    "max": "-",
                    "unique_values": "-",
                    "lcuv": "-",
                    "mcuv": "-",
                }
            )

        return features

    def get_model_version_history(self, model_id: str) -> list:
        """Get the feature importance for a model

        Args:
            model_id (str): ID of the model.

        Returns:
            list: feature importance statistics for the model.
        """
        model_infos = self.get_model_info_history(model_id)

        feature_history = []

        for model_info in model_infos:
            feature_history.append(
                {
                    "id": model_info["model_id"],
                    "name": model_info["model_metadata"]["model_name"],
                    "description": model_info["model_metadata"]["description"],
                    "status": model_info["model_metadata"]["status"],
                    "version": model_info["model_version"],
                    "trained_date": model_info["scheduled_date"],
                    "owner": model_info["model_metadata"]["owner"],
                    "lookback_window": model_info["model_metadata"][
                        "lookback_days"
                    ],
                    "prediction_window": model_info["model_metadata"][
                        "prediction_days"
                    ],
                    "fulcrum_date": model_info["model_metadata"][
                        "fulcrum_date"
                    ],
                }
            )

        return feature_history

    # TODO HUS-2969
    def get_model_pipeline_performance(self, model_id: str) -> dict:
        """Get the model performance of a model.

        Args:
            model_id (str): ID of the model.

        Returns:
            dict: pipeline performance statistics.
        """

        return {
            "training": {
                "id": model_id,
                "most_recent_run_duration": "-",
                "run_duration": [
                    {
                        "status": "-",
                        "timestamp": "-",
                        "duration": "-",
                    }
                ],
                "last_run": "-",
                "frequency": "-",
                "total_runs": "-",
            },
            "scoring": {
                "most_recent_run_duration": "-",
                "run_duration": [
                    {
                        "status": "-",
                        "timestamp": "-",
                        "duration": "-",
                    }
                ],
                "last_run": "-",
                "frequency": "-",
                "total_runs": "-",
            },
        }

    def get_model_lift(self, model_id: str) -> list:
        """Get the lift statics of a model.

        Args:
            model_id (str): ID of the model.

        Returns:
            list: lift statistics.
        """
        lift_stats = []
        model_info = self.get_model_info(model_id)

        for lift_info in model_info["lift_chart"]:
            lift_stats.append(
                {
                    "bucket": lift_info["bucket"],
                    "predicted_value": lift_info["predicted"],
                    "actual_value": lift_info["actual"],
                    "profile_count": lift_info["profiles"],
                    "predicted_rate": lift_info["rate_predicted"],
                    "actual_rate": lift_info["rate_actual"],
                    "predicted_lift": lift_info["lift_predicted"],
                    "actual_lift": lift_info["lift_actual"],
                    "profile_size_percent": lift_info["size_profile"],
                }
            )

        return lift_stats

    # TODO test
    def get_model_drift(self, model_id: str) -> list:
        """Get the drift statics of a model.

        Args:
            model_id (str): ID of the model.

        Returns:
            list: list of drift statistics.
        """
        model_infos = self.get_model_info_history(model_id)
        drift_data = []

        for model_info in model_infos:
            drift_data.append({
                "drift": model_info["model_metrics"]["AUC"],
                "run_date": datetime.strptime(model_info["scheduled_date"], "%Y-%m-%d")
            })

        return drift_data


if __name__ == "__main__":
    model_id = "model-Propensity_ctg_tk_blanket-v5-dev"
    print(Decisioning().get_all_model_ids())
    print(Decisioning().get_model_drift(model_id))
    # print(Decisioning().get_all_models())
    # print(Decisioning().get_health_status())
