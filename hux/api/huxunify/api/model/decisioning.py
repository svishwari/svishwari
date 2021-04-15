"""
The purpose of this file is for housing the Decisioning related API models
"""
from os import getenv
from random import randint
from urllib.parse import urlparse
from io import BytesIO
import Algorithmia
from Algorithmia.errors import AlgorithmException
import pandas as pd
from huxunify.api.data_connectors.aws import get_aws_client


# get tecton api key
TECTON_API_HEADERS = {
    "Authorization": f"Tecton-key {getenv('TECTON_API_KEY')}",
}

# set Algorithmia vars
ALGORITHMIA_KEY = getenv("ALGORITHMIA_API_KEY")
ALGORITHMIA_API = "https://api.algorithmia.hux-decisioning.in"
# TODO - get names of algorithms from Decision team
ALGORITHMS = ["dolong_deloitte_com/h2o_scores_to_stream"]


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

    def get_algorithms(self) -> list:
        """get algos from api.
        Args:

        Returns:
            list: list of algorithmia dictionary object
        """
        # get info for each one
        algos = [self.get_algorithm(algo) for algo in ALGORITHMS]

        # remove none values if any
        return [i for i in algos if i]

    def get_algorithm(self, algorithm_name: str) -> str:
        """get information for a specific algorithm
        Args:
            algorithm_name: id of data source

        Returns:
            str: json data of algorithmia dictionary object

        """
        try:
            # get algorithm details
            algo = self.client.algo(algorithm_name).info()
        except AlgorithmException:
            return None

        # extract all the available properties
        algo_cleaned_dict = self.translate_version_info(algo)

        # remove the thousand line statement of compilation notes of algo
        if "compilation" in algo_cleaned_dict:
            algo_cleaned_dict["compilation"].pop("output", None)
        return algo_cleaned_dict

    def translate_version_info(self, algo_response: dict) -> dict:
        """translate algo to dict
        TODO I am going to submit a PR to algorithmia to add this.
        TODO I will update their __dict__ VersionInfo function.
        Args:
            algo_response: algorimia dictionary object

        Returns:
            str: json data of algorithmia dictionary object

        """
        return_dict = {}
        for key in algo_response.attribute_map.keys():
            if hasattr(getattr(algo_response, key), "attribute_map"):
                return_dict[key] = self.translate_version_info(
                    getattr(algo_response, key)
                )
            else:
                return_dict[key] = getattr(algo_response, key)
        return return_dict

    def invoke_algorithm(
        self, algorithm_name: str, body: str, timeout_seconds: int = 60
    ):
        """invoke an algorithm
        Args:
            algorithm_name: algorithm name
            body: json data of scores
            timeout_seconds: timeout length

        Returns:
            str: algorithm result

        """
        # band-aid solution for this model,
        # algorithmia is currently missing a package needed
        # to run the model Jingjing built,
        # the package is h20, she has a ticket with them.
        if "h2o_scores_to_stream" in algorithm_name:
            body = prep_data_h2o_scores_to_stream(body)

        # setup algo
        algo = self.client.algo(algorithm_name)

        # set query parameters here
        algo.set_options(timeout=timeout_seconds, stdout=False)

        # get algo result
        return algo.pipe(body).result


def prep_data_h2o_scores_to_stream(data: str) -> str:
    """
    convert incoming data into JSON for streaming
    Args:
        data: hto scores

    Returns:
        str: algorithm result

    """
    # pull parquet file from s3
    s3_client = get_aws_client()

    # get bucket name from url
    s3_url_obj = urlparse(data)

    # get the file object,
    # ignore first character from url path to get s3 key
    s3_obj = s3_client.get_object(Bucket=s3_url_obj.netloc, Key=s3_url_obj.path[1:])

    # read the initial parquet data
    datafile = pd.read_parquet(BytesIO(s3_obj["Body"].read()))

    # clean the dataframe for pushing to algorithmia
    cleaned_df = datafile.iloc[[1]].dropna(axis=1)

    # return the JSON response
    return cleaned_df.to_json(orient="records")


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

    def get_features(self) -> None:
        """purpose of this function is for getting the features back for a customer
        Args:

        Returns:
        """
        # fake the request for now until we have access
        # response = requests.post
        # (f'https://{self.cluster_id}.tecton.ai/api/v1/feature-service
        # /get-features', headers=TECTON_API_HEADERS, data=data).json()
        self.features = ["imps_count_14d_1d", "imps_count_28d_1d", "imps_count_60d_1d"]

    def get_feature_vectors(self) -> None:
        """purpose of this function is for getting the feature vectors
        Args:

        Returns:
        """
        # check if any features to get vectors for
        if not self.features:
            return

        # fake the request for now until we have access
        # response = requests.post
        # (f'https://{self.cluster_id}.tecton.ai/api/v1/feature-service
        # /get_feature_vector', headers=TECTON_API_HEADERS, data=data).json()
        for feat in self.features:
            self.predictions.append({"feature": feat, "user_clicks": randint(1, 60)})
