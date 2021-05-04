# 1. Build the API

FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

MAINTAINER Jim McMahon <jimcmahon@deloitte.com>

WORKDIR /app/hux-unified/api
COPY ./lib /app/lib
COPY ./hux/api /app/hux-unified/api
COPY .pylintrc /app
COPY Pipfile* /app/hux-unified/api

# This line allows the env variable to be picked up from Codefresh
ARG ARTIFACTORY_PYTHON_READ
ARG JFROG_USERNAME
ARG JFROG_PASSWORD

# install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# lock current deps to make it easier for docker to build
RUN cd /app/hux-unified/api && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /app/hux-unified/api/requirements.txt

WORKDIR /app/hux-unified/api/huxunify
CMD ["flask", "run", "app.py"]
