=========
6.2 - TBD
=========

Release date:
TBD

Release Overview
-----------------
This and extension of the Hux 6.0 release, which is focused on making our technology stack operationally real. This includes the following goals:

- Client support
- Building out process between design and front-end team
- Audience segmentation improvements
- HX TrustID MVP completion
- Enhancements of decisioning data
- Demo enhancements



Data Management
---------------
All features that belong to decisioning including IDR, Data sources, and data source monitoring.

**********************
New Features & Updates
**********************
- Added SQL database to the standard Decisioning stack for new environments to enable data scientists to expedite client onboarding

*****
Fixes
*****
- Propensities Updated on CDM API
- CDM Testing of 5.0 schema
- CDM Realistic data in RC1 - continued support
- Pagination at Datasources dashboard
- Feature engineering enhancements by integrating with CDM for a client's NetSuite, Bluecore and Aqfer data sources



Decisioning
-----------
All features that belong to decisioning including models and model monitoring.

**********************
New Features & Updates
**********************
- Industry tagging for models
    - Models show specific industry tags
    - The user can filter models by an industry
    - When switching to demo mode under client settings, and selecting an industry, the models page will auto-filter by the selected industry

*****
Fixes
*****
- Improvements to Stub Data, making it more realistic
- Improved communication with Unified UI by refactoring the design of Decisioning API
- Availability of target scores for direct consumption by CDM and Unified UI
- Improvements in speed and accuracy of model training and scoring by automated feature ranking and dimensionality reduction
- Enhancements to the Standard Pipeline Framework by improvements in modularity of Kubeflow components, adding pipeline components for supporting wider ML Ops use-cases and increased reliability
- Enhanced system reliability by adding monitoring & alerting capability for the Decisioning API and Decisioning Sandbox and Production environments


Orchestration
-------------
All features that belong to orchestration including destinations, audiences, and engagements.

**********************
New Features & Updates
**********************
- Additional segmentation capabilities available based on event data
- Industry tagging for audiences
    - When creating an audience, a user can tag the audience with a specific industry
    - The user can filter the audience table by an industry
    - When switching to demo mode under client settings, and selecting an industry, the audience list will auto-filter by the selected industry


*****
Fixes
*****
- Support for Signals Router
    - Support in the delivery of all event type data to Google
- Audience filter enhancements on the audience table


Solutions
----------
This is a new area that was introduced as part of the 6.0 release. These are solutions and assets, outside of Hux, that have been introduced part of the Hux UI.

**********************
New Features & Updates
**********************
- Email delivery using KEDA
- HX TrustID MVP completion



Other Updates
-------------
Additional updates across the platform that do not belong to a specific module.

**********************
New Features & Updates
**********************
- Addition of “Client settings” under configuration
    - Ability for user to turn on demo mode which will add an industry-specific theme and labels across the UI
- Addition of CURA training and Documentation (which includes these release notes!) to the help menu in the top navigation
- Surfacing alerts to the side navigation when there is an errror in models, destinations, or data sources


*****
Fixes
*****
- Cypress code coverage
- Azure deployment support
- SendGrid email templates
- Alert and notification clean-up (I.e. simplifying what alerts show up in alerts and notifications)
- Notification Category Alert Improvements
- MongoDB Cert deployment
- Prometheus E2E test metric integration



In Progress
-----------
These are items that the team are currently working on adding into the UI that were not able to be completed as part of this release.

- Storybook component updates in the UI
- Additional audience segmentation improvements
- Client UI support
- Discovery for ingesting manual segments

