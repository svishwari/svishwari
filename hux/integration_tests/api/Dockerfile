# build the test environment
FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

# set the work dir on the docker image
WORKDIR /app/hux-unified/integration_tests/api

# copy over the hux/integration_tests/api folder from the host to the container
COPY . /app/hux-unified/integration_tests/api

# upgrade pip to the latest
RUN pip install pip --upgrade

# install pipenv packages
RUN pip install pytest
RUN pip install pymongo
RUN pip install requests

# run the pytests application
CMD ["py.test", "test/test_*.py", "-v"]
