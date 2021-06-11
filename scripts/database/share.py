"""
purpose of this file is housing any shared scripts for the
mongo stand-up scripts
"""
import os
from pathlib import Path
from pymongo import MongoClient


def get_mongo_client() -> MongoClient:
    """Get Mongo Client directly

    Args:
    Returns:
        MongoClient: A connected mongo client, pulling settings from the environment
    """
    # Get details on MongoDB configuration.
    env = dict(os.environ)
    host = env.get("MONGO_DB_HOST")
    port = int(env["MONGO_DB_PORT"]) if "MONGO_DB_PORT" in os.environ else None
    user_name = env.get("MONGO_DB_USERNAME")
    password = env.get("MONGO_DB_PASSWORD")
    # grab the SSL cert path
    use_ssl = host not in ["localhost", None]

    # Set up the database client
    if use_ssl:
        ssl_cert_path = str(Path(__file__).parent.joinpath("rds-combined-ca-bundle.pem"))
        db_client = MongoClient(
            host,
            port,
            w=1,
            username=user_name,
            password=password,
            ssl=True,
            ssl_ca_certs=ssl_cert_path,
        )
    else:
        db_client = MongoClient(
            host,
            port,
            w=1,
            username=user_name,
            password=password,
            ssl=use_ssl,
        )

    return db_client
