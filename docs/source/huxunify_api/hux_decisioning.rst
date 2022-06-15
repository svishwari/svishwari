Decisioning Connector
=====================

Details
-------

The Unified solution now retrieves its models and relevant data from Decisioning's Metrics API.

The API has two endpoints as follows:
    1. GET /models
        This endpoint retrieves a list of all the model ids.
    2. GET /model-info/<model_id>
        This endpoint retrieves a list of model info objects. There is one model info object for
        each version of the model.

The Decisioning team has provided a library, huxmodelclient, to connect to their API.

The data connector called Decisioning leverages this library. It contains simple functions
that can be called to retrieve the relevant data and map that data into the proper formats
that each respective endpoint needs.

The Unified API typically takes the access token that is provided by Okta as a header. The
Metrics API takes the idToken that is provided by Okta as a header. To resolve this, the Unified
UI will be sending the idToken in each request as well so that the Unified API will be able to
pass the idToken onto the Metrics API. This will change in the future to have the Metrics API
