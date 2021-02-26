"""
purpose of this file is testing the advertising performance router
"""
import json
from unittest import TestCase
from huxunify.app import create_app


class TestAdvertising(TestCase):
    """
    test all marketing routes
    """
    def setUp(self):
        """
        setup the initial test client
        """
        self.app = create_app().test_client()

    def test_index(self):
        """
        Tests the route screen message for the landing page
        """
        api_route = self.app.get('/api/marketing/')

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual({"message": 'Hello marketing'}, api_route.get_json())

    def test_fetch_models(self):
        """
        Tests the route for fetching models
        """
        api_route = self.app.post('/api/marketing/models')
        result = json.loads(api_route.data)
        self.assertEqual(3, len(result['Models'][0]))

    def test_segmentation(self):
        """
        Tests the route for the segmentation engine
        """
        payload = {
                   "url": "s3://xspdev-amc-pipeline/customers_names_e2e.csv",
                   "models": [
                      "Churn",
                      "Propensity"
                   ]
                  }
        api_route = self.app.post('/api/marketing/segmentation', data=json.dumps(payload),
                                  headers={'Content-Type': 'application/json'})
        result = json.loads(api_route.data)
        self.assertEqual(20, len(result['PredictionData']))

    def test_segmentation_on_the_fly(self):
        """
        Tests the route for the segmentation engine on the fly
        """
        payload = {
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
                                               "value": 0.6
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
           ]
        }
        api_route = self.app.post('/api/marketing/segmentation/fly', data=json.dumps(payload),
                                  headers={'Content-Type': 'application/json'})
        result = json.loads(api_route.data)
        self.assertEqual(2, len(result['PredictionData']))
