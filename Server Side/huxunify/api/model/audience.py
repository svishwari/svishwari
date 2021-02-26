"""
purpose of this file is for housing the audience models
"""
import requests

class AudienceModel:
    """
    audience model class

    Here is a sample model response from audience service
        [
            {
                "audience_filters": [
                    {
                        "field": "age",
                        "type": "max",
                        "value": 60
                    }
                ],
                "audience_name": "string",
                "audience_type": "string",
                "created": "2020-10-17T21:54:53.495000+00:00",
                "updated": "2020-10-17T21:54:53.495000+00:00",
                "audience_id": "5f5f7262997acad4bac4373b",
                "ingestion_job_id": "5f5f7262997acad4bac4373b"
            }
        ]
    """

    API = "https://audience-builder.main.use1.k8s.mgnt-xspdev.in/api/v1/audiences"
    TOKEN = '<Update OKTA token here for audience service access.>'

    def __init__(self):
        self.message = "Hello audience"
        self.audiences = []
        self.audience_name = ""
        self.audience_type = ""

    def get_audience_count(self):
        """
        purpose of this function is to get audience count
        :param data:
        :return:
        """
        # push the request
        return requests.get(f'{self.API}/count').json()

    def get_audiences(self):
        """
        purpose of this function is to get audiences
        :param data:
        :return:
        """
        # Make a request to audience service
        response = requests.get(f'{self.API}',
                                headers = {'Authorization': f'Bearer {self.TOKEN}'})
        print(response.json())
        return response.json()

    def get_audience_by_id(self, audience_id):
        """
        purpose of this function is to get audiences
        :param data:
        :return:
        """
        # Make a request to audience service
        # return requests.get(f'{self.API}').json()

        response = requests.get(f'{self.API}/{audience_id}',
                                headers = {'Authorization': f'Bearer {self.TOKEN}'})
        return response.json()

    def create_audiences(self, data):
        """
        purpose of this function is to create audiences
        :param data:
        :return:
        """
        # push the request
        return requests.post(f'{self.API}/audiences', data=data).json()

    def update_audiences(self, data):
        """
        purpose of this function is to update audiences
        :param data:
        :return:
        """
        # push the request
        return requests.put(f'{self.API}/audiences', data=data).json()

    def delete_audiences(self, audience_id):
        """
        purpose of this function is to update audiences
        :param data:
        :return:
        """
        # push the request
        return requests.delete(f'{self.API}/audiences/{audience_id}').json()

    def star_audiences(self, audience_id):
        """
        purpose of this function is to update audiences
        :param data:
        :return:
        """
        # push the request
        # return requests.delete(f'{self.API}/audiences/{audience_id}/star').json()
        return "star_audiences mock"

    def get_recent_audiences(self):
        """
        purpose of this function is to get recent audiences
        :param data:
        :return:
        """
        # push the request
        # return requests.get(f'{self.API}/audiences/recent').json()
        return "get_recent_audiences mock"

    def get_star_audiences(self):
        """
        purpose of this function is to get recent audiences
        :param data:
        :return:
        """
        # push the request
        # return requests.get(f'{self.API}/audiences/star').json()
        return "get_star_audiences mock"

    def get_audience_delivery_jobs(self, audience_id):
        """
        purpose of this function is to get audience delivery jobs for an audience
        :param data:
        :return:
        """
        # push the request
        # return requests.get(f'{self.API}/audiences/{audience_id}/deliveries').json()
        return "get_audience_delivery_jobs mock"
