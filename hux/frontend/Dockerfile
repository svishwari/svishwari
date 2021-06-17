# application environment variables
FROM huxhub.repo.mgnt.in/alpine:latest AS base
ARG OKTA_ISSUER
ARG OKTA_CLIENT_ID
ARG API_URL
RUN echo -e "VUE_APP_OKTA_ISSUER=$OKTA_ISSUER" \
    "\nVUE_APP_OKTA_CLIENT_ID=$OKTA_CLIENT_ID" \
    "\nVUE_APP_API_URL=$API_URL" \ > /tmp/env_file

# build environment
FROM huxhub.repo.mgnt.in/node:lts-alpine as huxui-build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
RUN yarn ci
RUN yarn global add @vue/cli@4.5.6
COPY . /app
COPY --from=base /tmp/env_file .env
RUN yarn test:unit
RUN yarn build

# production environment
FROM huxhub.repo.mgnt.in/nginx:alpine
COPY --from=huxui-build /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
