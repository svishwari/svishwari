"""
purpose of this file is for housing the advertising models
"""
import requests


# HARDCODED HEADERS, temporary solution.
CODE_HEADERS = {
    "authority": "audience-builder.main.use1.k8s.mgnt-xspdev.in",
    # TODO - manually copying token from browser for now, not the best, but at least it works
    #  for testing
    "authorization": "Bearer ####",
    "accept": "application/json, text/plain, */*",
}


class AdvertisingModel:
    """
    advertising model class
    """

    API = "https://audience-builder.main.use1.k8s.mgnt-xspdev.in/api/v1"

    def __init__(self):
        self.message = "Hello advertising"

    def get_data_sources(self) -> str:
        """purpose of this function is to get all data sources
        Args:

        Returns:
            str: json data

        """
        # push the request
        result = requests.get(f"{self.API}/data-sources", headers=CODE_HEADERS).json()
        return result

    def get_data_sources_count(self) -> int:
        """purpose of this function is to get the count of all data sources
        Args:

        Returns:
            int: count of data sources

        """

        # push the request
        result = requests.get(f"{self.API}/data-sources", headers=CODE_HEADERS).json()
        return len(result)

    def create_data_source(self, data: str):
        """purpose of this function is to create a data source
        Args:
            data: json data for data source

        Returns:
            str: json data

        """
        # push the request
        url = f"{self.API}/data-sources"
        obj = requests.post(url, json=data, headers=CODE_HEADERS)
        return obj.json()

    def update_data_source(self, data_source_id: int, data: str):
        """
        purpose of this function is to update a data source
        Args:
            data_source_id: id of data source
            data: json data for data source

        Returns:
            str: json data

        """
        # push the request
        url = f"{self.API}/data-sources/{data_source_id}"
        obj = requests.put(url, json=data, headers=CODE_HEADERS)
        return obj.json()

    def delete_data_source(self, data_source_id: int) -> str:
        """purpose of this function is to delete a data source
        # TODO method is not ready in Audience Builder yet.
        Args:
            data_source_id: id of data source

        Returns:
            str: json data

        """
        # push the request
        return requests.delete(f"{self.API}/data-sources/{data_source_id}").json()

    @staticmethod
    # pylint: disable=W0613
    def star_data_source(data_source_id: int) -> str:
        """purpose of this function is to star a data source
        # TODO method is not ready in Audience Builder yet.
        Args:
            data_source_id: id of data source

        Returns:
            str: json data

        """
        # return requests.get(f'{self.API}/data-sources/{data_source_id}?star={star}').json()
        return "star data source mock, not available in Audience builder yet"

    def validate_data_source(self, data_source_id: int) -> str:
        """purpose of this function is to validate a data source
        Args:
            data_source_id: id of data source

        Returns:
            str: json data

        """
        # push the request, perhaps this is a post/put, or this is Update Datasource??
        return requests.get(f"{self.API}/data-sources/{data_source_id}").json()

    def get_destination_count(self) -> int:
        """purpose of this function is to get delivery platform count
        # TODO method is not ready in Audience Builder yet.
        Args:

        Returns:
            int: destination count

        """
        destinations = requests.get(
            f"{self.API}/delivery-platforms", headers=CODE_HEADERS
        ).json()
        return len(destinations)

    def get_delivery_platforms(self) -> str:
        """purpose of this function is to get all delivery platforms
        Args:

        Returns:
            str: json data

        """
        return requests.get(
            f"{self.API}/delivery-platforms", headers=CODE_HEADERS
        ).json()

    def create_delivery_platform(self, data: str) -> str:
        """purpose of this function is to create a delivery platform
        Args:
            data: json data for delivery platform
        Returns:
            str: json data

        """

        url = f"{self.API}/delivery-platforms"
        obj = requests.post(url, json=data, headers=CODE_HEADERS)
        return obj.json()

    def update_delivery_platform(self, delivery_platform_id: int, data: str) -> str:
        """purpose of this function is to update a delivery platform
        Args:
            delivery_platform_id: id of the delivery platform
            data: json data for delivery platform
        Returns:
            str: json data

        """

        return requests.put(
            f"{self.API}/delivery-platforms/{delivery_platform_id}",
            json=data,
            headers=CODE_HEADERS,
        ).json()

    @staticmethod
    # pylint: disable=W0613
    def star_delivery_platform(data: str) -> str:
        """purpose of this function is to update a delivery platform
        # TODO method is not ready in Audience Builder yet.
        Args:
            data: json data for delivery platform
        Returns:
            str: json data

        """
        # return requests.put(f'{self.API}/delivery-platforms', data=data).json()
        return "star_delivery_platform mock, not available in Audience builder yet"

    def validate_delivery_platform(self, delivery_platform_id: int) -> str:
        """purpose of this function is to validate a delivery platform
        Args:
            delivery_platform_id: id of the delivery platform
        Returns:
            str: json data

        """
        return requests.put(
            f"{self.API}/delivery-platforms/{delivery_platform_id}"
        ).json()
