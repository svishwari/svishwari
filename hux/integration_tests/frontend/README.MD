# Integration tests

This is to run integration tests that cover end-to-end functionality of the
Unified UI, via the UI through to the underlying API, database and
services.

## Pre-requisites

Ensure you have the complete application and services running within an
environment and that these integration tests have access to this environment.

This includes the following.
- UI
- API
- Database
- Services
  - Okta

## Getting started

Install integration tests dependencies.

```sh
npm install
```

Run the integration tests in headless mode (CLI).

```sh
npm run test
```

Run the integration tests in browser with the Cypress app.

```sh
npm run test:dev
```