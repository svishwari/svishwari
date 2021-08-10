"""
Purpose of this script is for storing unittests
"""
import logging

# disable debug logs for requests mock.
logging.getLogger("requests_mock").setLevel(logging.WARNING)
