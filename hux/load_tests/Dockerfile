# build the test environment
FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified
FROM huxhub.repo.mgnt.in/locustio/locust AS locust

# set the work dir on the docker image
WORKDIR /app/hux/load_tests

# copy over the hux/api folder from the host to the container
COPY . /app/hux/load_tests

# upgrade pip to the latest
RUN pip install pip --upgrade

# install pipenv
RUN pip install locust

# run the locust load test application
EXPOSE 8089
CMD ["locust"]
