"""Purpose of this file is housing any shared scripts for the mongo stand-up
scripts.
"""
import os
from pathlib import Path
from pymongo import MongoClient


def get_mongo_client() -> MongoClient:
    """Get Mongo Client directly.

    Returns:
        MongoClient: A connected mongo client, pulling settings from the
            environment.
    """

    # Get details on MongoDB configuration.
    host = os.environ.get("MONGO_DB_HOST")
    port = int(os.environ["MONGO_DB_PORT"]) if "MONGO_DB_PORT" in os.environ else None
    user_name = os.environ.get("MONGO_DB_USERNAME")
    password = os.environ.get("MONGO_DB_PASSWORD")
    use_ssl = host not in ["localhost", None]

    mongo_config = dict(
        host=host,
        port=port,
        w=1,
        username=user_name,
        password=password,
        ssl=use_ssl,
    )

    if use_ssl:
        # grab the SSL cert path
        mongo_config["ssl_ca_certs"] = str(
            Path(__file__).parent.joinpath("rds-combined-ca-bundle.pem")
        )

    return MongoClient(**mongo_config)
