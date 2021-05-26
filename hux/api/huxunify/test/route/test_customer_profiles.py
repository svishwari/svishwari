
import unittest
import requests
import json
import sys


class TestCustomerProfilesOverview(unittest.TestCase):
    """
    Sample JSON Response

    {
        "gender_men": 0.46123,
        "gender_other": 0.02123,
        "gender_women": 0.52123,
        "match_rate": 0.60123,
        "max_age": 11,
        "min_age": 25,
        "total_cities": 12,
        "total_countries": 27,
        "total_customers": 45214665,
        "total_household_ids": 75341415,
        "total_individual_ids": 36795473,
        "total_known_ids": 47087690,
        "total_records": 56597152,
        "total_unique_ids": 12090374,
        "total_unknown_ids": 85082591,
        "total_us_states": 52,
        "updated": "2021-05-26T16:04:56.006790"
    }
    """
    def test_count_insights(self):
        """
        It tests the count of values of Customer Profile Overviews
        
        Expected Count=17
        """
        response = requests.get('http://localhost:5000/api/v1/customer/overview')
        self.assertEqual(len(response.json()),17)
 
    def test_gender_ratios(self):
        """
        It tests the gender ratios to be greater than 0 and sum should be equal to 1

        """
        response = requests.get('http://localhost:5000/api/v1/customer/overview')
        gender_men=response.json()['gender_men']
        gender_women=response.json()['gender_women']
        gender_other=response.json()['gender_other']
        
        sum_gender=gender_men+gender_women+gender_other
        
        self.assertGreaterEqual(gender_men,gender_women,0)
        self.assertGreaterEqual(gender_women,0)
        self.assertGreaterEqual(gender_other,0)

        self.assertEqual(round(sum_gender,2),1.00)

    def test_age(self):
        """
        It tests that minimum age to be greater than 19
        and maximum age to be less than 90

        also minimum age to be less than maximum age
        """
        response = requests.get('http://localhost:5000/api/v1/customer/overview')
        min_age=response.json()['min_age']
        max_age=response.json()['max_age']

        self.assertGreaterEqual(min_age,19)
        self.assertLessEqual(max_age,90)
        self.assertLess(min_age,max_age)

    def test_records(self):
        """
        It tests that the records should be greater than 0
        """
        response = requests.get('http://localhost:5000/api/v1/customer/overview')
        total_records=response.json()['total_records']
        total_known_ids=response.json()['total_known_ids']
        total_unknown_ids=response.json()['total_unknown_ids']

        self.assertGreater(total_known_ids,0)
        self.assertGreater(total_unknown_ids,0)
        self.assertGreater(total_records,0)

if __name__ == "__main__":
    unittest.main()