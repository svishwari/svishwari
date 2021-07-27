# 1. Build the Test Image

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

# set the working directory again
#WORKDIR /app/hux-unified/api

# run the pytests application
# pip install
# RUN pip install python-box
# append hux-unified integration_tests path to python path.
#ENV PYTHONPATH "${PYTHONPATH}:/app/hux-unified/integration_tests/api"
CMD ["py.test", "test_core.tavern.yaml", "-v"]
