"""
The purpose of this file is for housing the Decisioning related API models
"""
from random import randint
from huxunify.api import config


# get tecton api key
TECTON_API_HEADERS = {
    "Authorization": f"Tecton-key {config.TECTON_API_KEY}",
}


class DecisionModel:
    """
    Decisioning model class
    """

    def __init__(self):
        self.message = "Hello Decisioning"


class CustomerFeatureModel:
    """
    See all features per customer
    """

    def __init__(self, cluster_id, feature_service_name, customer_id):
        self.cluster_id = cluster_id
        self.feature_service_name = feature_service_name
        self.customer_id = customer_id
        self.message = "List all features for a customer"
        self.features = []
        self.predictions = []

    def get_features(self):
        """
        purpose of this function is for getting the features back for a customer
        :return:
        """
        # fake the request for now until we have access
        # response = requests.post
        # (f'https://{self.cluster_id}.tecton.ai/api/v1/feature-service
        # /get-features', headers=TECTON_API_HEADERS, data=data).json()
        self.features = [
            "imps_count_14d_1d",
            "imps_count_28d_1d",
            "imps_count_60d_1d",
        ]

    def get_feature_vectors(self):
        """
        purpose of this function is for getting the feature vectors
        :return:
        """
        # check if any features to get vectors for
        if not self.features:
            return

        # fake the request for now until we have access
        # response = requests.post
        # (f'https://{self.cluster_id}.tecton.ai/api/v1/feature-service
        # /get_feature_vector', headers=TECTON_API_HEADERS, data=data).json()
        for feat in self.features:
            self.predictions.append(
                {"feature": feat, "user_clicks": randint(1, 60)}
            )
