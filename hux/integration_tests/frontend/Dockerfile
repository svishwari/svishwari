FROM cypress/base:10
WORKDIR /app
COPY package*.json /app/
RUN npm ci
RUN $(npm bin)/cypress verify
COPY . /app