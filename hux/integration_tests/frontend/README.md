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
npm test
```

Run the integration tests with additional parameters, such as video enabled.

```sh
npm test -- --config video=true
```

For more parameters, refer to the [Cypress docs](https://docs.cypress.io/guides/references/configuration#Options)
and [specifically for videos](https://docs.cypress.io/guides/references/configuration#Videos).

Run the integration tests in browser with the Cypress app.

```sh
npm run test:dev
```

## Running in a dedicated environment

To run the integration/end-to-end tests in a dev environment, use the following
configuration below.

Here is the example configuration to run in dev.

| `baseUrl`                                            | `USER_EMAIL`                         | `USER_PASSWORD`                      |
| ---------------------------------------------------- | ------------------------------------ | ------------------------------------ |
| https://unified-ui-dev.main.use1.hux-unified-dev1.in | See 1Password: Unified Dev Test User | See 1Password: Unified Dev Test User |

1. Ensure you are connected to the dev VPN and are able to access the `baseUrl` from your browser.

2. Run `npm test` with the configured additional parameters:

```sh
npm test -- --config baseUrl=https://unified-ui-dev.main.use1.hux-unified-dev1.in --env USER_EMAIL=<...>,USER_PASSWORD=<...>
```

3. You can also update both `cypress.json` for configuration and
   `cypress.env.json` for environment variables:

```json
// cypress.json
{
  "baseUrl": "https://unified-ui-dev.main.use1.hux-unified-dev1.in",
  "chromeWebSecurity": false,
  "video": false
}
```

```json
// cypress.env.json
{
  "USER_EMAIL": "<...>",
  "USER_PASSWORD": "<...>"
}
```

These will run the tests locally against the dedicated environment in dev.

**Note**:

Tests are also built and run with CI/CD pipelines, with any merge to main.
They are run in the staging environment.

## Running with Docker

### Pre-requisites

Have the UI running locally configured for Docker's needs using the following.

```sh
cd ../../frontend
yarn serve:docker
```

Verify its running and accessible from https://host.docker.internal:9090

### Build

```sh
docker build --no-cache -f Dockerfile -t ui-integration-tests .
```

### Run

Run the tests, using your defined configuration and environment variables.

```sh
docker run ui-integration-tests npm run test -- --config baseUrl=https://host.docker.internal:9090 --env FOO=foo,BAR=bar
```

To avoid environment variables being packaged with the build, we ignore any
environment variables configured in `cypress.env.**.json` and instead define
the environment variables at run time.

Here is an example run with custom configuration and environment variables,
where we have exported both our configuration (eg. baseUrl) and environment
variables (eg. USER_EMAIL and USER_PASSWORD) and passed them in at runtime.

```sh
export CYPRESS_BASE_URL=https://host.docker.internal:9090
export CYPRESS_USER_EMAIL=<e2e_test_user_email>
export CYPRESS_USER_PASSWORD=<e2e_test_user_password>
```

```sh
docker run --ipc=host ui-integration-tests npm run test -- --config baseUrl=$CYPRESS_BASE_URL,video=true --env USER_EMAIL=$CYPRESS_USER_EMAIL,USER_PASSWORD=$CYPRESS_USER_PASSWORD
```

To review/debug test runs, mount volumes for the tests, logs and outputs.

```sh
export CYPRESS_LOGS="$(pwd)"/logs:/root/.npm/_logs
export CYPRESS_DEV="$(pwd)"/cypress:/app/cypress
docker run -it --ipc=host -v $CYPRESS_LOGS -v $CYPRESS_DEV ui-integration-tests npm run test -- --config baseUrl=$CYPRESS_BASE_URL,video=true --env USER_EMAIL=$CYPRESS_USER_EMAIL,USER_PASSWORD=$CYPRESS_USER_PASSWORD
```

These are useful for debugging runs locally, where you can view the tests'
output logs, screenshots and videos directly.
