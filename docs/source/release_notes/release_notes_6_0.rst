===
6.0
===

:Release Date: 
May 5, 2022


Release Overview
================

This Hux 6.0 release was focused on making our technology stack operationally real. This includes the following goals: 
* We can easily connect a wide range of customer data types
* Integrated environments and test with real data; validating the platform is operational end-to-end
* We can use real customer data to characterize and powerfully differentiate the needs and values of individual or segments of consumers
* Improve our performance across all endpoints

Data Management
===============

All features that belong to decisioning including IDR, Data sources, and data source monitoring.

New Features & Updates
----------------------
* Click into a data source's feed and see the list of files that have been processed
* Ability to remove a pending data source
* More data source options

Decisioning
============

All features that belong to decisioning including models and model monitoring.

New Features & Updates
----------------------
* Ability to request a model
* Ability to remove a requested model
* Introduction of model categories
* Version history enhancement
** User can click on a model version history and see past information of a particular model

Fixes
-----
* Improvements to performance for the model dashboards
* Triggering actions on failures on backend
* Health check failures

Orchestration
=============

All features that belong to orchestration including destinations, audiences, and engagements.

New Features & Updates
----------------------
* Destination enhancements
** Remove a connected (Active) destination
** Ability to request a destination
** Additional destination options
** Destination categories
** Open a destination via a URL
* Engagement enhancements
** Ability to remove an engagement
** Ability to filter engagements
** Delivery schedule: Select a time range and specific time for when you want audiences to be delivered automatically
* Audience enhancements
** Ability to remove an audience
** Ability for standalone deliveries (i.e. the delivery of an audience without being part of an engagement)
* Updates to customer overview dashboard
* Segment playground: Allowing the ability to play with your customer data before creating an audience
** Ability to segment by customer events

Other Updates
=============

Additional updates across the platform that do not belong to a specific module.

New Features & Updates
----------------------
* Contact us: Available from the top navigation under the "?" icon
** Submit feedback
** Contact / Email us
** Submit a bug
* Ability to track any created issues from the UI under "My Issues" and auto-create a JIRA ticket
* Configuration: Located in the left hand navigation. This area contains insights into who has access to a client as well as what is configured
** Requesting a team member
** View teammembers
** Access levels for users (Admin, View-only, and Edit)
** View the configuration of a particular client's modules and solutions
** Control who can and cannot see PII data
* Backend support for multi-tenancy
* Enhancements to alerts
** Filtering
** Setting up email notifications for alerts 
* New Solutions 
** Email Deliverability Dashboard
* Add "Need Help?" Section on homepage

Fixes
-----
* Create blockers to stop real data from leaving our system
* IDR Matching Trends Graph performance
* Audience dashboard performance
* Improvements to end to end testing
* Improvements on notifications
* Stabilize pipeline for all environments

In Progress
=============

These are items that the team are currently working on adding into the UI that were not able to be completed as part of this release. 

* HX TrustID
* Azure deployment
* Modular architecture
* Pipeline monitoring dashboard
* Validating match rate & audience size from Google and Facebook
* Replace audience option in a delivered destination
