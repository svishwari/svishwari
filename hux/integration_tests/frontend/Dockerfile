FROM huxhub.repo.mgnt.in/cypress/base:latest
WORKDIR /app
COPY package*.json /app/
RUN npm ci
RUN $(npm bin)/cypress verify
COPY . /app
CMD ["npm", "run", "test"]
