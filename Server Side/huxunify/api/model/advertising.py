"""
purpose of this file is for housing the advertising models
"""
import requests


class AdvertisingModel:
    """
    advertising model class
    """
    API = "https://audience-builder.main.use1.k8s.mgnt-xspdev.in/api/v1/ui"

    def __init__(self):
        self.message = "Hello advertising"

    def get_data_sources(self):
        """
        purpose of this function is to get all data sources
        :param data:
        :return:
        """
        # push the request
        return requests.get(f'{self.API}/data-sources').json()

    def create_data_source(self, data):
        """
        purpose of this function is to create a data source
        :param data:
        :return:
        """
        # push the request
        return requests.post(f'{self.API}/data-sources', data=data).json()

    def update_data_source(self, data):
        """
        purpose of this function is to update a data source
        :param data:
        :return:
        """
        # push the request
        return requests.put(f'{self.API}/data-sources', data=data).json()

    def delete_data_source(self, data_source_id):
        """
        purpose of this function is to delete a data source
        :param data:
        :return:
        """
        # push the request
        return requests.delete(f'{self.API}/data-sources/{data_source_id}').json()

    def star_data_source(self, data_source_id, star=True):
        """
        purpose of this function is to star a data source
        :param data:
        :return:
        """
        # push the request, perhaps this is a post/put, or this is Update Datasource??
        # return requests.get(f'{self.API}/data-sources/{data_source_id}?star={star}').json()
        return "star data source mock"

    def validate_data_source(self, data_source_id, star=True):
        """
        purpose of this function is to validate a data source
        :param data:
        :return:
        """
        # push the request, perhaps this is a post/put, or this is Update Datasource??
        # return requests.get(f'{self.API}/data-sources/{data_source_id}?star={star}').json()
        return "validate_data_source mock"

    def get_destination_count(self):
        """
        purpose of this function is to get delivery platform count
        :param data:
        :return:
        """
        # return requests.get(f'{self.API}/delivery-platforms/count').json()
        return "get_destination_count mock"

    def get_delivery_platforms(self):
        """
        purpose of this function is to get all delivery platforms
        :param data:
        :return:
        """
        return requests.get(f'{self.API}/delivery-platforms').json()

    def create_delivery_platform(self, data):
        """
        purpose of this function is to create a delivery platform
        :param data:
        :return:
        """
        return requests.post(f'{self.API}/delivery-platforms', data=data).json()

    def update_delivery_platform(self, data):
        """
        purpose of this function is to update a delivery platform
        :param data:
        :return:
        """
        return requests.put(f'{self.API}/delivery-platforms', data=data).json()

    def star_delivery_platform(self, data, star=True):
        """
        purpose of this function is to update a delivery platform
        :param data:
        :return:
        """
        # return requests.put(f'{self.API}/delivery-platforms', data=data).json()
        return "star_delivery_platform mock"

    def validate_delivery_platform(self, delivery_platform_id):
        """
        purpose of this function is to validate a delivery platform
        :param data:
        :return:
        """
        # return requests.put(f'{self.API}/delivery-platforms', data=data).json()
        return "validate_delivery_platform mock"

    def get_audience_count(self):
        """
        purpose of this function is to get audience count
        :param data:
        :return:
        """
        # push the request
        return requests.get(f'{self.API}/audiences/count').json()

    def get_audiences(self):
        """
        purpose of this function is to get audiences
        :param data:
        :return:
        """
        # push the request
        return requests.get(f'{self.API}/audiences').json()

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
