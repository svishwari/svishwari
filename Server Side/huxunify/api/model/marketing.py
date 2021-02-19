"""
purpose of this file is for housing the marketing models
"""
from random import randint, random


class MarketingModel:
    """
    marketing model class

    segment information/values = Segmentation_Engine.Segmentation_scores
    segments = Segmentation_Engine.Segmentation_Logs  # holistic level, not customer level
    """
    SEGMENT_API = "https://amc-segmentation.main.use1.k8s.mgnt-xspdev.in/app"

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
        query = 'SELECT count(*) as segment_count FROM Segmentation_Engine.segmentation_scores'
        self.segment_count = randint(1, 1000)

    def get_all_segment_runs(self):
        """
        pass
        :return:
        """
        segments = []
        for i in range(0, randint(1, 100)):
            segments.append({
                "TransactionId": i
            })
        return segments

    def create_segment(self):
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
                            "0.81-1.0": "Very likely"
                        },
                        "Values": {
                            "Min": round(0 + (0.1-0) * random(), 2),
                            "Max": round(0.8 + (1-0.8) * random(), 2)
                        }
                    }
            }
        }

    def update_segment(self, segment):
        """
        pass
        :return:
        """
        return {
            "Scales": {
                    "Propensity": {
                        "Segments": {
                            "0.0-0.2": "Unlikely",
                            "0.81-1.0": "Very likely"
                        },
                        "Values": {
                            "Min": round(0 + (0.1-0) * random(), 2),
                            "Max": round(0.8 + (1-0.8) * random(), 2)
                        }
                    }
            }
        }

    def get_segment_run(self, segment_id):
        """
        pass
        :return:
        """
        prediction_data = []
        for i in range(0, randint(1, 50)):
            prediction_data.append({
                "User": i,
                "Segment": "Most Likely"
            })
        return {
            "TransactionId": segment_id,
            "PredictionData": prediction_data
        }

    def get_segment_customers(self, segment_id):
        """
        pass
        :return:
        """
        customers = []
        for i in [randint(0, 40) for iter in range(30)]:
            customers.append({
                "CustomerId": i,
            })
        return {
            "customers": customers
        }

    def get_models(self, category):
        """
        purpose of this function is for getting the models from the api
        :return:
        """
        data = {
            "params": {
                "Category": f"{category}"
            }
        }

        # fake the request for now until I have access
        # response = requests.post(f'{SEGMENT_API}/model/fetchModels', data=data).json()
        self.models = [
            {
                "name": "Churn",
                "value": "1",
            },
            {
                "name": "Propensity",
                "value": "2",
            },
            {
                "name": "LTV",
                "value": "3",
            }
        ]

    def get_scores(self, s3_url, models):
        """
        purpose of this function is for getting the scores from the api
        :return:
        """
        data = {
           "url": s3_url,
           "Models": models
        }

        # fake the request for now until I have access
        # response = requests.post(f'{SEGMENT_API}/public/segmentation', data=data).json()
        self.segments =[{
               "PredictionData": [
                  {
                        "User": "A5BB0719-2CE0-762B-7C68-C67361766A18",
                        "Segment": "Most Likely"
                  }
               ],
               "fileURL": "s3://XXXXXXXX/customers.csv",
               "TransactionID": "260fecbf-3bd9-4a70-8c4c-0a174f708e46",
               "Scales": {
                  "Churn": {
                        "Segments": {
                           "0.0-0.2": "Unlikely",
                           "0.21-0.5": "Likely",
                           "0.51-0.8": "Most likely",
                           "0.81-1.0": "Very likely"
                        },
                        "Values": {
                           "Min": "0.0",
                           "Max": "1.0"
                        }
                  },
                  "Propensity": {
                        "Segments": {
                           "0.0-0.2": "Unlikely",
                           "0.21-0.5": "Likely",
                           "0.51-0.8": "Most likely",
                           "0.81-1.0": "Very likely"
                        },
                        "Values": {
                           "Min": "0.0",
                           "Max": "1.0"
                        }
                  }
               }
            }]

    def get_scores_on_the_fly(self, body):
        """
        purpose of this function is for getting the scores from the api
        :return:
        """
        # fake the request for now until I have access
        # return requests.post(f'{SEGMENT_API}/public/segmentOnFly', data=body).json()
        self.segments = [
            {
               "TransactionID": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
               "Scales": {
                  "Propensity": {
                        "Segments": {
                           "0.0-0.2": "Unlikely",
                           "0.21-0.5": "Likely",
                           "0.51-0.8": "Most likely",
                           "0.81-1.0": "Very likely"
                        },
                        "Values": {
                           "Min": "0.0",
                           "Max": "1.0"
                        }
                  }
               },
               "Rules": [
                  {
                        "Rule": [
                           {
                              "Transaction": {
                                    "all": [
                                       {
                                          "all": [
                                                {
                                                   "fact": "Propensity",
                                                   "operator": "greaterThanInclusive",
                                                   "value": 0.35
                                                },
                                                {
                                                   "fact": "Propensity",
                                                   "operator": "lessThanInclusive",
                                                   "value": 1
                                                }
                                          ]
                                       }
                                    ]
                              }
                           },
                           {
                              "Values": {
                                    "Segment": "Most Likely"
                              }
                           }
                        ]
                  }
               ],
               "PredictionData": [
                  {
                        "User": "1",
                        "Segment": "Most Likely"
                  },
                  {
                        "User": "2"
                  }
               ]
            }
        ]

    def deliver_segment(self, body):
        """
        purpose of this function is for delivering the segment
        :return:
        """
        # fake the request for now until I have access
        # response = requests.post(f'{SEGMENT_API}/public/segmentOnFly', data=body).json()
        self.status = "Triggered"
