# End-to-end tests

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

## Running with Docker

### Pre-requisites

Have the UI running locally over `https` using the following.

```sh
cd ../../frontend
yarn server --https
```

### Build

```sh
docker build -f Dockerfile -t ui-integration-tests .
```

### Run

Set the base URL for the tests.

```sh
export CYPRESS_BASE_URL=https://host.docker.internal:8080
```

Run the tests, using the provided configuration and environment variables.
```sh
docker run ui-integration-tests npm run test -- --config baseUrl=$CYPRESS_BASE_URL --env FOO=$CYPRESS_FOO,BAR=$CYPRESS_BAR
```

To review/debug test runs, mount volumes for test logs and outputs.

```sh
export CYPRESS_LOGS="$(pwd)"/logs:/root/.npm/_logs
export CYPRESS_VIDEOS="$(pwd)"/cypress/videos:/app/cypress/videos
export CYPRESS_SCREENSHOTS="$(pwd)"/cypress/screenshots:/app/cypress/screenshots
docker run -it -v $CYPRESS_LOGS -v $CYPRESS_VIDEOS -v $CYPRESS_SCREENSHOTS ui-integration-tests npm run test -- --config baseUrl=$CYPRESS_BASE_URL
```
