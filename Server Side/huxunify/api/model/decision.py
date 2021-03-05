"""
The purpose of this file is for housing the Decisioning related API models
"""
from os import getenv
from random import randint
import Algorithmia
from Algorithmia.errors import AlgorithmException


# get tecton api key
TECTON_API_HEADERS = {
    'Authorization': f"Tecton-key {getenv('TECTON_API_KEY')}",
}

# set Algorithmia vars
ALGORITHMIA_KEY = getenv('ALGORITHMIA_API_KEY')
ALGORITHMIA_API = 'https://api.algorithmia.hux-decisioning.in'
# TODO - get names of algorithms from Decision team
ALGORITHMS = ['dolong_deloitte_com/hux_unified_test',
              'demo/Hello', 'mansoshaik_deloitte_com/iris_xgboost',
              'mlaclavik_deloitte_com/test_lightgbm']


class DecisionModel:
    """
    Decisioning model class
    """
    def __init__(self):
        self.message = "Hello Decisioning"


class AlgorithmiaModel:
    """
    Decisioning model class
    """
    def __init__(self):
        # initialize the algorithmia connection object
        self.client = Algorithmia.client(ALGORITHMIA_KEY, ALGORITHMIA_API)

    def get_algorithms(self):
        """
        get algos from api.
        :return: list of algo
        """
        # get info for each one
        algos = [self.get_algorithm(algo) for algo in ALGORITHMS]

        # remove none values if any
        return [i for i in algos if i]

    def get_algorithm(self, algorithm_name):
        """
        get information for a specific algorithm
        :return: algorithmia dictionary object
        """
        try:
            # get algorithm details
            algo = self.client.algo(algorithm_name).info()
        except AlgorithmException:
            return None

        # extract all the available properties
        algo_cleaned_dict = self.translate_version_info(algo)

        # remove the thousand line statement of compilation notes of algo
        if 'compilation' in algo_cleaned_dict:
            algo_cleaned_dict['compilation'].pop('output', None)
        return algo_cleaned_dict

    def translate_version_info(self, algo_response):
        """
        translate algo to dict
        I am going to submit a PR to algorithmia to add this.
        I will update their __dict__ VersionInfo function.
        """
        return_dict = {}
        for k, v in algo_response.attribute_map.items():
            if hasattr(getattr(algo_response, k), 'attribute_map'):
                return_dict[k] = self.translate_version_info(getattr(algo_response, k))
            else:
                return_dict[k] = getattr(algo_response, k)
        return return_dict

    def invoke_algorithm(self, algorithm_name, body, timeout_seconds=60):
        """
        invoke an algorithm
        :return:
        """
        # band-aid solution for this model, algorithmia is currently missing a package needed
        # to run the model Jingjing built, the package is h20, she has a ticket with them.
        if algorithm_name == 'dolong_deloitte_com/hux_unified_test':
            return [
                {
                    "predict":0,
                    "p0":0.9997829795,
                    "p1":0.0002170039,
                    "user_cookie":"0070b377e0214941a7e5267c9f96b6ab"
                }
            ]

        # setup algo
        algo = self.client.algo(algorithm_name)

        # set query parameters here
        algo.set_options(timeout=timeout_seconds, stdout=False)

        # get algo result
        return algo.pipe(body).result


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
