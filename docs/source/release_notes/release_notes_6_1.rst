===
6.1
===

Release date:
June 3, 2022

Release Overview
-----------------
This and extension of the Hux 6.0 release, which is focused on making our technology stack operationally real. This includes the following goals:

- Integrated environments and test with real data; validating the platform is operational end-to-end
- We can now use real customer data to characterize and powerfully differentiate the needs and values of individual or segments of consumers
- Improve our performance across all endpoints
- Integration of TrustID
- Azure deployment


Decisioning
-----------
All features that belong to decisioning including models and model monitoring.

**********************
New Features & Updates
**********************
- Pipeline monitoring: Gain insights about a model scores, runs, and failures
- Enhancements to features table with more realistic data


Orchestration
-------------
All features that belong to orchestration including destinations, audiences, and engagements.

**********************
New Features & Updates
**********************
- Audience Replacement: Ability for a user to choose to have an audience auto-replaced in a destination
- Ability to create lookalike audiences as a single delivery (standalone delivery)
- Event segmentation

*****
Fixes
*****
- Improving performance for Lookalike audience
- Audience response time improvement


Solutions
----------
This is a new area that was introduced as part of the 6.0 release. These are solutions and assets, outside of Hux, that have been introduced part of the Hux UI.

**********************
New Features & Updates
**********************
- TrustID: Understand your customer's trust scores based off survey data

*****
Fixes
*****
- Email Deliverability
     - Error and empty states
     - Open rate hover enhancements


Other Updates
-------------
Additional updates across the platform that do not belong to a specific module.

**********************
New Features & Updates
**********************
- Configuration enhancements
     - Ability to enable demo mode and customize branding for a particular client industry and user
     - Ability for an admin to remove a user
     - Ability for an admin to edit a user's access level
- General bug fixes
- Release enhancements to RC1

*****
Fixes
*****
- Permission enhancements: Elimination of CTAs based on user access level
     - Clean up of alerting based off access level
- DAST reports vulnerability
- Health checks and logging


In Progress
-----------
These are items that the team are currently working on adding into the UI that were not able to be completed as part of this release.

- Enhancements to our development process
     - Building out of reusable components to increase speed and efficiency in development
- Azure deployment
- Discovery on deploying UI without CDP (CDP lite)
- Enhancements to segmentation

Decisioning
============

This is a quick overview of high level changes.

New Features
-------------

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
accept the access token.
