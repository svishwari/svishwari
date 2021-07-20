# 1. Build the Test Image

FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

# set the work dir on the docker image
WORKDIR /app/hux-unified/integration_tests

# copy over the hux/api folder from the host to the container
COPY ./hux/integration_tests /app/hux-unified/integration_tests

# upgrade pip to the latest
RUN pip install pip --upgrade

# install pipenv
RUN pip install pytest
RUN pip install tavern

# set the working directory again
WORKDIR /app/hux-unified/api

# run the pytests application
RUN py.test -v
