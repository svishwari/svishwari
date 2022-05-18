===
6.0
===

:Date: May 5, 2022


Release Overview
================

This page is intended to house the release notes for the 6.0 release. This is a brief high level description of the main initiatives.
as an example: This Hux 5.2 release was focused on improving the UI demo experience and resolving known issues since our MVP release in October. Design enhancements were made globally and are most evident for Data Sources, Customer Profiles, and Destinations. Certain performance issues and non-intuitive user flows have been resolved. Few new features were added.


Data Management
===============

This is a quick overview of high level changes.

New Features
-------------

* List item
* List item
* List item

Fixes
-----

* List item
* List item
* List item

Other Changes
-------------

* List item
* List item
* List item


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

Orchestration
=============

This is a quick overview of high level changes.

New Features
-------------

* List item
* List item
* List item

Fixes
-----

* List item
* List item
* List item

Other Changes
-------------

* List item
* List item
* List item


Other Updates
=============

This is a quick overview of high level changes.

New Features
-------------

* List item
* List item
* List item

Fixes
-----

* List item
* List item
* List item

Other Changes
-------------

* List item
* List item
* List item
