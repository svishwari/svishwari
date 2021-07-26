# Hux UI

## Project setup
```sh
yarn install
```

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

### Lints and fixes files
```sh
yarn lint
```

> **💡 PRO TIPS**
> 1. If your branch's CI is failing but locally your lint and/or
> unit tests are passing (or vice versa), try a fresh install locally:
>    ```sh
>    rm -rf node_modules
>    yarn install # or yarn ci
>    ```
>    This should clear up most issues.
>
> 2. Use **`yarn <command>`** — <ins>do not</ins> use **`npm <command>`** and
> remove `package-lock.json` if somehow you ended up with one locally.

### Run storybook

```sh
yarn serve:storybook
```

## Docker

Build.

```sh
docker build --build-arg API_URL="http://unified-api-dev.main.use1.hux-unified-dev1.in" --build-arg OKTA_ISSUER="https://dev-631073.okta.com" --build-arg OKTA_CLIENT_ID="0oa2wbure49NQsL7a4x7" -t hux-ui .
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
    |https://localhost:8080/login/callback|https://localhost:8080/login|https://localhost:8080/login|
    |https://host.docker.internal:8080/login/callback|https://host.docker.internal:8080/login|-|

4. Configure the Trusted Origins (`Security > API > Trusted Origins tab`) with the base URI of our frontend app:

    |Origin URL|Type|
    |-|-|
    |https://localhost:8080|CORS|
    |https://host.docker.internal:8080|CORS|

  > NOTE: We have included redirect URIs and base URIs specifically to run end-to-end integration tests with Docker locally using the special DNS name `host.docker.internal`

5. Use the Okta app's Client ID and dev URL in the env configuration for the frontend app.
