from http import HTTPStatus
from typing import Tuple

import pymongo
from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView
import datetime

from huxunifylib.database import (
    constants as db_constants,
    notification_management,
)
from huxunify.api.schema.customer_profiles import CustomerProfilesOverview
from huxunify.api.route.utils import add_view_to_blueprint, get_db_client
from huxunify.api.schema.utils import AUTH401_RESPONSE
import huxunify.api.constants as c

from random import randint

CUSTOMER_PROFILES_TAG = "customer-profiles"
CUSTOMER_PROFILES_DESCRIPTION = "Customeer Profiles API"
CUSTOMER_PROFILES_OVERVIEW_ENDPOINT = "/customer/overview"

# setup the notifications blueprint
customer_profiles_bp = Blueprint(CUSTOMER_PROFILES_OVERVIEW_ENDPOINT, import_name=__name__)


@add_view_to_blueprint(
    customer_profiles_bp, f"/{CUSTOMER_PROFILES_OVERVIEW_ENDPOINT}", "CustomerProfilesOverview")
class CustomerProfilesOverview(SwaggerView):
    """
    Customer Profiles Overview class
    """
    
    responses = {
        HTTPStatus.OK.value: {
            "description": "Customer Profiles Overview",
            "schema": {"type": "array", "items": CustomerProfilesOverview},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [CUSTOMER_PROFILES_TAG]

    @marshal_with(CustomerProfilesOverview)
    def get(self) -> Tuple[dict,int]:
        """Retrieves Customer Profiles Overview.

        ---

        Returns:
            Tuple[dict, int] dict of Customer Profile Overview and http code
        """
        response={
                    c.TOTAL_RECORDS:randint(10000000,99999999),
                    c.MATCH_RATE:0.60123,
                    c.TOTAL_UNIQUE_IDS:randint(10000000,99999999),
                    c.TOTAL_UNKNOWN_IDS:randint(10000000,99999999),
                    c.TOTAL_KNOWN_IDS:randint(10000000,99999999),
                    c.TOTAL_INDIVIDUAL_IDS:randint(10000000,99999999),
                    c.TOTAL_HOUSEHOLD_IDS:randint(10000000,99999999),
                    c.UPDATED:datetime.datetime.now(),
                    c.TOTAL_CUSTOMERS:randint(10000000,99999999),
                    c.COUNTRIES:randint(1,100),
                    c.STATES:randint(1,100),
                    c.CITIES:randint(10^3,10^5-1),
                    c.MIN_AGE:randint(1,100),
                    c.MAX_AGE:randint(1,100),
                    c.GENDER_WOMEN:0.52123,
                    c.GENDER_MEN:0.46123,
                    c.GENDER_OTHER:0.02123
                }
       
      
       
        return response,HTTPStatus.OK
