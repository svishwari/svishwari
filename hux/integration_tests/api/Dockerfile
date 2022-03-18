# build the test environment
FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified
FROM huxhub.repo.mgnt.in/locustio/locust AS locust

# set the work dir on the docker image
WORKDIR /app/hux-unified/integration_tests/api

# copy over the hux/api folder from the host to the container
COPY . /app/hux-unified/integration_tests/api

# upgrade pip to the latest
RUN pip install pip --upgrade

# install pipenv
RUN pip install pytest
RUN pip install pymongo
RUN pip install locust

# run the pytests application
# append hux-unified integration_tests api path to python path
ENV PYTHONPATH "${PYTHONPATH}:/app/hux-unified/integration_tests/api"
CMD ["py.test", "-v"]
CMD ["--locustfile", "locustfile.py", \
        "--headless", \
        "--users", "2", \
        "--spawn-rate", "20", \
        "--run-time", "200"]
