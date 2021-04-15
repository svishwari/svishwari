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
    TOKEN = "<Auth token goes here>"

    def __init__(self):
        self.message = "Hello audience"
        self.audiences = []
        self.audience_name = ""
        self.audience_type = ""

    def get_audience_count(self):
        """
        purpose of this function is to get audience count
        :return:
        """
        # push the request
        return requests.get(f"{self.API}/count").json()

    def get_audiences(self) -> str:
        """purpose of this function is to get audiences
        Args:

        Returns:
            str: json data

        """
        # Make a request to audience service
        response = requests.get(
            f"{self.API}", headers={"Authorization": f"Bearer {self.TOKEN}"}
        )
        return response.json()

    def get_audience_by_id(self, audience_id) -> str:
        """purpose of this function is to get audiences

        Args:
            param audience_id: id of audience

        Returns:
            str: json data

        """
        # Make a request to audience service
        # return requests.get(f'{self.API}').json()

        response = requests.get(
            f"{self.API}/{audience_id}",
            headers={"Authorization": f"Bearer {self.TOKEN}"},
        )
        return response.json()

    def create_audiences(self, data: str) -> str:
        """purpose of this function is to create audiences

        Args:
            data: json data for audience

        Returns:
            str: json data

        """
        # push the request
        response = requests.post(
            f"{self.API}", json=data, headers={"Authorization": f"Bearer {self.TOKEN}"}
        )
        return response.json()

    def update_audiences(self, data: str) -> str:
        """purpose of this function is to update audiences
        Args:
            data: json data for audience

        Returns:
            str: json data

        """
        # push the request
        response = requests.put(
            f"{self.API}", json=data, headers={"Authorization": f"Bearer {self.TOKEN}"}
        )
        return response.json()

    def delete_audiences(self, audience_id: int) -> str:
        """purpose of this function is to update audiences
        Args:
            param audience_id: id of audience

        Returns:
            str: json data

        """
        # push the request
        response = requests.delete(
            f"{self.API}/{audience_id}",
            headers={"Authorization": f"Bearer {self.TOKEN}"},
        )
        return response.json()

    def get_audience_delivery_jobs(self, audience_id: int) -> str:
        """purpose of this function is to get audience delivery jobs for an audience
        Args:
            audience_id: id of audience

        Returns:
            str: json data

        """
        # push the request
        response = requests.get(
            f"{self.API}/{audience_id}/deliveries",
            headers={"Authorization": f"Bearer {self.TOKEN}"},
        )
        print(response)
        return response.json()

    def create_audience_delivery_job(self, audience_id: int, data: str) -> str:
        """purpose of this function is to create audiences
        Args:
            audience_id: id of audience
            data: json data for audience

        Returns:
            str: json data

        """
        # push the request
        response = requests.post(
            f"{self.API}/{audience_id}/deliveries",
            json=data,
            headers={"Authorization": f"Bearer {self.TOKEN}"},
        )
        return response.json()

    def get_audience_insights(self, audience_id: int) -> str:
        """purpose of this function is to get audience insights for an audience
        Args:
            audience_id: id of audience

        Returns:
            str: json data

        """

        # push the request
        return requests.get(
            f"{self.API}/{audience_id}/insights",
            headers={"Authorization": f"Bearer {self.TOKEN}"},
        ).json()

    def get_delivery_job_by_audience_id(
        self, audience_id: int, delivery_job_id: int
    ) -> str:
        """purpose of this function is to get audience delivery jobs for an audience
        Args:
            audience_id: id of audience
            delivery_job_id: id of delivery job

        Returns:
            str: json data

        """

        # push the request
        return requests.get(
            f"{self.API}/{audience_id}/deliveries/{delivery_job_id}",
            headers={"Authorization": f"Bearer {self.TOKEN}"},
        ).json()

    def get_insights_delivery_job_audience_id(
        self, audience_id: int, delivery_job_id: int
    ) -> str:
        """purpose of this function is to get audience delivery jobs for an audience
        Args:
            audience_id: id of audience
            delivery_job_id: id of delivery job

        Returns:
            str: json data

        """
        # push the request
        return requests.get(
            f"{self.API}/{audience_id}/deliveries/{delivery_job_id}/insights",
            headers={"Authorization": f"Bearer {self.TOKEN}"},
        ).json()
