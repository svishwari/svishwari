"""
purpose of this file is for housing the marketing models
"""
from random import randint, random
import requests


class MarketingModel:
    """
    marketing model class

    segment information/values = Segmentation_Engine.Segmentation_scores
    segments = Segmentation_Engine.Segmentation_Logs  # holistic level, not customer level
    """

    # this should be configurable
    SEGMENT_API = "https://amc-segmentation.main.use1.k8s.mgnt-xspdev.in/app"
    SEGMENT_ENGINE = f"{SEGMENT_API}/segmentationengine"

    def __init__(self):
        self.message = "Hello marketing"
        self.models = []
        self.segments = []
        self.status = ""
        self.segment_count = 0

    def get_number_of_segment_runs(self):
        """
        get count of segments
        :return:
        """
        # query = 'SELECT count(*) as segment_count FROM Segmentation_Engine.segmentation_scores'
        self.segment_count = randint(1, 1000)

    @staticmethod
    def get_all_segment_runs():
        """
        pass
        :return:
        """
        segments = []
        for i in range(0, randint(1, 100)):
            segments.append({"TransactionId": i})
        return segments

    @staticmethod
    def create_segment():
        """
        pass
        :return:
        """
        return {
            "TransactionID": "bbbf8785734-2c39-4f2b-8cb6-e6b837d93ac0",
            "Scales": {
                "Propensity": {
                    "Segments": {
                        "0.0-0.2": "Unlikely",
                        "0.21-0.5": "Likely",
                        "0.51-0.8": "Most likely",
                        "0.81-1.0": "Very likely",
                    },
                    "Values": {
                        "Min": round(0 + (0.1 - 0) * random(), 2),
                        "Max": round(0.8 + (1 - 0.8) * random(), 2),
                    },
                }
            },
        }

    @staticmethod
    # pylint: disable=W0613
    def update_segment(segment):
        """
        pass
        :return:
        """
        return {
            "Scales": {
                "Propensity": {
                    "Segments": {
                        "0.0-0.2": "Unlikely",
                        "0.81-1.0": "Very likely",
                    },
                    "Values": {
                        "Min": round(0 + (0.1 - 0) * random(), 2),
                        "Max": round(0.8 + (1 - 0.8) * random(), 2),
                    },
                }
            }
        }

    @staticmethod
    def get_segment_run(segment_id):
        """
        pass
        :return:
        """
        prediction_data = []
        for i in range(0, randint(1, 50)):
            prediction_data.append({"User": i, "Segment": "Most Likely"})
        return {"TransactionId": segment_id, "PredictionData": prediction_data}

    @staticmethod
    # pylint: disable=W0613
    def get_segment_customers(segment_id):
        """
        pass
        :return:
        """
        customers = []
        for i in [randint(0, 40) for iter in range(30)]:
            customers.append(
                {
                    "CustomerId": i,
                }
            )
        return {"customers": customers}

    def get_models(self):
        """
        get models from the segmentation API

        Args:
        Returns:
            The return list of models from the segmentation API

        """
        return requests.post(f"{self.SEGMENT_API}/model/fetchModels").json()

    def get_scores(self, s3_url, models):
        """Fetch the Segmentation Model Scores

        Args:
            data: input json string

        Returns:
            Returns the post result

        """
        data = {"url": s3_url, "Models": models}
        return requests.post(
            f"{self.SEGMENT_ENGINE}/segmentation", data=data
        ).json()

    def get_segment_count(self):
        """Fetch the Segmentation Model Scores

        Args:
            data: input json string

        Returns:
            Returns the post result

        """
        return requests.get(
            f"{self.SEGMENT_ENGINE}/retrieveJourneyCount"
        ).json()

    def get_scores_on_the_fly(self, data):
        """Fetch the Segmentation Model Scores on the fly
        this api allows for grouping of segments.

        Args:
            data: input json string

        Returns:
            Returns the post result

        """
        headers = {
            "content-type": "application/json",
            "cache-control": "no-cache",
        }
        return requests.post(
            f"{self.SEGMENT_ENGINE}/segmentOnFly", data=data, headers=headers
        ).json()

    # pylint: disable=W0613
    def deliver_segment(self, body):
        """
        purpose of this function is for delivering the segment
        :return:
        """
        # fake the request for now until I have access
        # response = requests.post(f'{SEGMENT_API}/public/segmentOnFly', data=body).json()
        self.status = "Triggered"
