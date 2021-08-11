# base
FROM huxhub.repo.mgnt.in/node:lts-alpine AS base
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
RUN yarn global add @vue/cli@4.5.6

# dependencies
FROM base as dependencies
WORKDIR /app
RUN yarn ci

# test
FROM dependencies AS test
WORKDIR /app
COPY . /app

# build
FROM dependencies AS build
WORKDIR /app
ARG OKTA_ISSUER
ARG OKTA_CLIENT_ID
ARG API_URL
RUN echo -e "VUE_APP_OKTA_ISSUER=$OKTA_ISSUER" \
    "\nVUE_APP_OKTA_CLIENT_ID=$OKTA_CLIENT_ID" \
    "\nVUE_APP_API_URL=$API_URL" \ > .env
COPY --from=dependencies /app/node_modules ./node_modules
COPY . /app
RUN yarn build

# release
FROM huxhub.repo.mgnt.in/nginx:alpine as release
COPY --from=build /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
