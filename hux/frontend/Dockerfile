# application environment variables
FROM alpine:latest AS base
ARG OKTA_ISSUER
ARG OKTA_CLIENT
ARG API_URL
RUN echo -e "VUE_APP_OKTA_ISSUER=$OKTA_ISSUER" \
    "\nVUE_APP_OKTA_CLIENT_ID=$OKTA_CLIENT" \
    "\nVUE_APP_API_URL=$API_URL" \ > /tmp/env_file

# build environment
FROM node:14 as huxui-build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
RUN npm install
RUN npm install @vue/cli@4.5.6 -g
COPY . /app
COPY --from=base /tmp/env_file .env
RUN npm run build

# production environment
FROM nginx:1.16.0-alpine
COPY --from=huxui-build /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
