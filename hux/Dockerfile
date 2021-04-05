# 1. Build the API

FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

MAINTAINER Jim McMahon <jimcmahon@deloitte.com>

WORKDIR /app/hux-unified/api
COPY ./lib /app/lib
COPY ./hux/api /app/hux-unified/api
COPY .pylintrc /app

# install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# This line allows the env variable to be picked up from Codefresh
ARG ARTIFACTORY_PYTHON_READ

# install all dependencies listed in Pipfile
RUN pipenv install --deploy --pypi-mirror ${ARTIFACTORY_PYTHON_READ}

WORKDIR /app/hux-unified/api/huxunify
CMD ["pipenv", "run", "app.py"]