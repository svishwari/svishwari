# base
FROM huxhub.repo.mgnt.in/node:lts-alpine AS base
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock

# dependencies
FROM base as dependencies
WORKDIR /app
RUN yarn ci

# test
FROM dependencies AS test
WORKDIR /app
COPY . /app
RUN yarn global add @vue/cli

# build
FROM dependencies AS build
WORKDIR /app
ARG OKTA_ISSUER
ARG OKTA_CLIENT_ID
ARG API_URL
ARG BUILD_STORYBOOK
RUN echo -e "VUE_APP_OKTA_ISSUER=$OKTA_ISSUER" \
    "\nVUE_APP_OKTA_CLIENT_ID=$OKTA_CLIENT_ID" \
    "\nVUE_APP_API_URL=$API_URL" \ > .env
COPY --from=dependencies /app/node_modules ./node_modules
COPY . /app
RUN yarn build
RUN if [ "$BUILD_STORYBOOK" = "true" ] ; then yarn storybook:build ; fi

# release
FROM huxhub.repo.mgnt.in/nginx:alpine as release
COPY --from=build /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
RUN sed -i '5 i # Replace the default okta value & api url with env specific env data' /docker-entrypoint.sh && \
    sed -i '6 i FILENAME=$(ls /usr/share/nginx/html/js | grep "^app.*.js$")' /docker-entrypoint.sh && \
    sed -i '7 i sed -i "s|0oab1i3ldgYyRvk5r2p7|${VUE_APP_OKTA_CLIENT_ID}|g" /usr/share/nginx/html/js/$FILENAME' /docker-entrypoint.sh && \
    sed -i '8 i sed -i "s|https://unified-api-dev.main.use1.hux-unified-dev1.in|${VUE_APP_API_URL}|g" /usr/share/nginx/html/js/$FILENAME' /docker-entrypoint.sh

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
