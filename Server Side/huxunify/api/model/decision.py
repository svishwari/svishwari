"""
The purpose of this file is for housing the Decisioning related API models
"""
from os import getenv
from random import randint
from pathlib import Path
import requests
import Algorithmia


# get tecton api key
TECTON_API_HEADERS = {
    'Authorization': f"Tecton-key {getenv('TECTON_API_KEY')}",
}

# get ALGORITHMIA_API_KEY
ALGORITHMIA_API_KEY = getenv('ALGORITHMIA_API_KEY')


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
        self.algo_client = Algorithmia.client(ALGORITHMIA_API_KEY)
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
        data = {
            "params": {
                "feature_service_name": f"{self.feature_service_name}",
                "join_key_map": {
                    "user_cookie": f"{self.customer_id}"
                }
            }
        }

        # fake the request for now until we have access
        # response = requests.post(f'https://{self.cluster_id}.tecton.ai/api/v1/feature-service
        # /get-features', headers=TECTON_API_HEADERS, data=data).json()
        self.features = ['imps_count_14d_1d', 'imps_count_28d_1d', 'imps_count_60d_1d']

    def get_feature_vectors(self):
        """
        purpose of this function is for getting the feature vectors
        :return:
        """
        # check if any features to get vectors for
        if not self.features:
            return

        data = {
            "params": {
                "features": self.features,
                "join_key_map": {
                    "user_cookie": f"{self.customer_id}"
                }
            }
        }

        # fake the request for now until we have access
        # response = requests.post(f'https://{self.cluster_id}.tecton.ai/api/v1/feature-service
        # /get_feature_vector', headers=TECTON_API_HEADERS, data=data).json()
        for feat in self.features:
            self.predictions.append(
                {
                    'feature': feat,
                    'user_clicks': randint(1, 60)
                }
            )

    def get_scores_algo(self):
        """
        purpose of this function is to call the Algorithmia API to score the file

        there are two ways to score the file, the current method I could find
        is using the Algorithmia python SDK, however API would be preferred
        :return:
        """
        # initialize the algorithm
        algo = self.algo_client.algo('jcb_dg/external_lightgbm_demo_model/0.1.0')

        # create the temporary payload
        data = {
                "model_path": "",
                "scoring_file_path": "",
                "experiment_id": randint(1, 1000000)
            }
        # set the timeout
        algo.set_options(timeout=300)

        # generate the results
        result_path = algo.pipe(data).result

        # download the predictions scores
        result_file = self.algo_client.file(result_path).getFile()

        # load file into numpy
        # result = numpy.load(result_file.name)
        self.predictions = [3, 5, 6, 8, 2, 3]
