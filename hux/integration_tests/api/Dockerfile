# application environment variables
ARG TAVERN_TEST_HOST_ARG
ARG TAVERN_TEST_API_VERSION_ARG
RUN echo -e "TAVERN_TEST_HOST=$TAVERN_TEST_HOST_ARG" \
    "\TAVERN_TEST_API_VERSION=$TAVERN_TEST_API_VERSION_ARG" \ > /tmp/env_file

# build the test environment
FROM python:3.7-slim-buster AS hux-unified

# set the work dir on the docker image
WORKDIR /app/hux-unified/integration_tests/api

# copy over the hux/api folder from the host to the container
COPY . /app/hux-unified/integration_tests/api

# upgrade pip to the latest
RUN pip install pip --upgrade

# install pipenv
RUN pip install pytest
RUN pip install tavern
RUN pip install python-box

# set the working directory again
#WORKDIR /app/hux-unified/api

# run the pytests application
# add tavern test host and api version as environment variables
ENV TAVERN_TEST_HOST "$TAVERN_TEST_HOST_ARG"
ENV TAVERN_TEST_API_VERSION "$TAVERN_TEST_API_VERSION_ARG"
# append hux-unified integration_tests api path to python path
#ENV PYTHONPATH "${PYTHONPATH}:/app/hux-unified/integration_tests/api"
#CMD ["py.test", "test_core.tavern.yaml", "-v"]
