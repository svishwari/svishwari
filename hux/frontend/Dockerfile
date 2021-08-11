# base
FROM huxhub.repo.mgnt.in/node:lts-alpine AS base
ARG OKTA_ISSUER
ARG OKTA_CLIENT_ID
ARG API_URL
RUN echo -e "VUE_APP_OKTA_ISSUER=$OKTA_ISSUER" \
    "\nVUE_APP_OKTA_CLIENT_ID=$OKTA_CLIENT_ID" \
    "\nVUE_APP_API_URL=$API_URL" \ > /tmp/env_file
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock

# dependencies
FROM base as dependencies
WORKDIR /app
RUN yarn global add @vue/cli@4.5.6
RUN yarn ci
COPY --from=base /tmp/env_file .env

# test
FROM dependencies AS test
WORKDIR /app
COPY . /app
RUN yarn lint
RUN yarn test:unit

# build
FROM dependencies AS build
WORKDIR /app
COPY --from=dependencies /app/node_modules ./node_modules
COPY . /app
RUN yarn build

# serve
FROM huxhub.repo.mgnt.in/nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
