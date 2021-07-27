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
yarn serve --https
```

### Build

```sh
docker build --no-cache -f Dockerfile -t ui-integration-tests .
```

### Run

Run the tests, using your defined configuration and environment variables.

```sh
docker run ui-integration-tests npm run test -- --config baseUrl=https://host.docker.internal:8080 --env FOO=foo,BAR=bar
```

To avoid environment variables being packaged with the build, we ignore any
environment variables configured in `cypress.env.**.json` and instead define
the environment variables at run time.

Here is an example run with custom configuration and environment variables,
where we have exported both our configuration (eg. baseUrl) and environment
variables (eg. USER_EMAIL and USER_PASSWORD) and passed them in at runtime.

```sh
export CYPRESS_BASE_URL=https://host.docker.internal:8080
export CYPRESS_USER_EMAIL=<e2e_test_user_email>
export CYPRESS_USER_EMAIL=<e2e_test_user_password>
```

```sh
docker run ui-integration-tests npm run test -- --config baseUrl=$CYPRESS_BASE_URL,video=true --env USER_EMAIL=$CYPRESS_USER_EMAIL,USER_PASSWORD=$CYPRESS_USER_PASSWORD
```

To review/debug test runs, mount volumes for test logs and outputs.

```sh
export CYPRESS_LOGS="$(pwd)"/logs:/root/.npm/_logs
export CYPRESS_VIDEOS="$(pwd)"/cypress/videos:/app/cypress/videos
export CYPRESS_SCREENSHOTS="$(pwd)"/cypress/screenshots:/app/cypress/screenshots
docker run -it -v $CYPRESS_LOGS -v $CYPRESS_VIDEOS -v $CYPRESS_SCREENSHOTS ui-integration-tests npm run test -- --config baseUrl=$CYPRESS_BASE_URL
```

These are useful for debugging runs locally, where you can view the tests'
output logs, screenshots and videos directly.
