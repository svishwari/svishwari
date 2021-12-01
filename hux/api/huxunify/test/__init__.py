"""Purpose of this script is for storing unittests."""
import logging
from os import environ
from huxunify.api import constants as db_c

# disable debug logs for requests mock.
logging.getLogger("requests_mock").setLevel(logging.WARNING)

# set flask env to test.
environ[db_c.FLASK_ENV] = db_c.TEST_MODE
