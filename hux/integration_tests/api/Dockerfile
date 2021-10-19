# build the test environment
FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

# set the work dir on the docker image
WORKDIR /app/hux-unified/integration_tests/api

# copy over the hux/api folder from the host to the container
COPY . /app/hux-unified/integration_tests/api

# upgrade pip to the latest
RUN pip install pip --upgrade

# install pipenv
RUN pip install pytest
RUN pip install pyperclip
RUN pip install tavern
RUN pip install python-box

# run the pytests application
# append hux-unified integration_tests api path to python path
ENV PYTHONPATH "${PYTHONPATH}:/app/hux-unified/integration_tests/api"
CMD ["py.test", "test_api_spec.tavern.yaml", "test_core.tavern.yaml", "test_data_sources.tavern.yaml", "test_notifications.tavern.yaml", "-v"]
# test_campaign.tavern.yaml mapping values are not allowed here?
# test_customers.tavern.yaml 4F 2P
# test_delivery.tavern.yaml 4F 2P
# test_destinations.tavern.yaml 5F 5P
# test_engagements.tavern.yaml 1F
# test_models.tavern.yaml
# test_orchestration.tavern.yaml 4F
# test_user.tavern.yaml 1F