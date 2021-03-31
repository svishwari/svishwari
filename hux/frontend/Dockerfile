# build environment
FROM node:14 as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json
RUN npm install --no-optional && npm cache clean --force
COPY . /app
# COPY --from=base /tmp/env_file .env
RUN npm run build

# production environment
FROM nginx
COPY --from=build /app/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]