# Hux UI

## Setup
```sh
yarn install
```

Pre-commit hooks will also be installed.
If not or you need to re-install them, then run:

```sh
yarn prepare
```

This will set you up with git pre-commit hooks and pre-push hooks that will run
your code changes against lint, style and tests before opening a pull request.

### Compiles and hot-reloads for development
```sh
yarn serve
```

### Compiles and minifies for production
```sh
yarn build
```

### Run your unit tests
```sh
yarn test:unit
```

#### Snapshots
If you have updated a reusable component's template, be sure to update the
snaphots for them and commit them with your changes using:

```sh
yarn test:unit -u
```

### Lint
```sh
yarn lint
```

> **💡 PRO TIPS**
> 1. If your branch's CI is failing but locally your lint and/or
> unit tests are passing (or vice versa), try a fresh install locally:
>    ```sh
>    rm -rf node_modules
>    yarn install
>    ```
>    This should clear up most issues.
>
> 2. Use **`yarn <command>`** — <ins>do not</ins> use **`npm <command>`** and
> remove `package-lock.json` if somehow you ended up with one locally.

### Style

```sh
yarn style
```

If there are style issues, run `yarn style:fix` to fix them.

### Run storybook

```sh
yarn serve:storybook
```

## Dev

To connect your localhost to the API in dev, do the following:

1. Create a `.env.dev1` by copying the `.env.local` configuration.
    ```sh
    cp .env.local .env.dev1
    ```
2. Update the `VUE_APP_API_URL` in `.env.dev1` to the hostname for the API in dev
    ```
    // .env.dev1
    ...
    VUE_APP_API_URL = https://unified-api-dev.main.use1.hux-unified-dev1.in
    ```

3. Restart your local development server using the new configuration.
    ```sh
    yarn serve --mode dev1
    ```
    Note: `--mode` allows you to use a different env file for your local server.

You will also need to create a `token.txt` file to store your temporary dev access token.

4. Create the token.txt file in `src/api/mock/token.txt`
    ```sh
    echo -e 'REPLACE_WITH_TOKEN' > src/api/mock/token.txt
    ```

5. Replace your token in `token.txt` with the one generated in dev.

You should now be able to open http://localhost:8080 and connect with the dev API.

You can verify this in the Network tab in your browser and Mirage will console out
with `Mirage: Passthrough request for <API request>`.

## Docker

Test.

```sh
docker build --target test -t hux-ui-dev .
docker run -it hux-ui-dev yarn lint
docker run -it hux-ui-dev yarn test:unit
```

Build.

```sh
docker build --target serve --build-arg API_URL="http://unified-api-dev.main.use1.hux-unified-dev1.in" --build-arg OKTA_ISSUER="https://dev-631073.okta.com" --build-arg OKTA_CLIENT_ID="0oa2wbure49NQsL7a4x7" -t hux-ui .
```

Run.

```sh
docker run -p 8080:80 hux-ui
```


Preview.

```sh
open http://localhost:8080
```

## Okta

For local development, we used a shared Okta dev account, configured as below:

```
VUE_APP_OKTA_CLIENT_ID=0oa2wbure49NQsL7a4x7
VUE_APP_OKTA_ISSUER=https://dev-631073.okta.com
```

To set up your own Okta dev account for local development, use the following
official guide from Okta:

- https://developer.okta.com/docs/guides/sign-into-spa/vue/before-you-begin

From the guide, you will need to

1. Signup for a [new dev account](https://developer.okta.com/signup).

2. Create an [Okta app](https://developer.okta.com/docs/guides/sign-into-spa/vue/create-okta-application).

3. Configure the Okta app for our frontend app:

    |Sign-in redirect URIs|Sign-out redirect URIs|Initiate login URI|
    |-|-|-|
    |http://localhost:8080/login/callback|http://localhost:8080/login|http://localhost:8080/login|
    |https://host.docker.internal:9090/login/callback|https://host.docker.internal:9090/login|-|

4. Configure the Trusted Origins (`Security > API > Trusted Origins tab`) with the base URI of our frontend app:

    |Origin URL|Type|
    |-|-|
    |http://localhost:8080|CORS|
    |https://host.docker.internal:9090|CORS|

  > NOTE: We have included redirect URIs and base URIs specifically to run end-to-end integration tests with Docker locally using the special DNS name `host.docker.internal`

5. Assign your user(s) to the app.

6. Use the Okta app's Client ID and dev URL in the `.env.local` configuration for the frontend app.
