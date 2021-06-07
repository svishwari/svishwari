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
