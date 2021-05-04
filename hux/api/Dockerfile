# 1. Build the API

FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

MAINTAINER Jim McMahon <jimcmahon@deloitte.com>

WORKDIR /app/hux-unified/api
COPY ./lib /app/lib
COPY ./hux/api /app/hux-unified/api
COPY .pylintrc /app

# This line allows the env variable to be picked up from Codefresh
ARG ARTIFACTORY_PYTHON_READ
ARG JFROG_USERNAME
ARG JFROG_PASSWORD

# install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# lock current deps to make it easier/faster for docker to build
RUN pipenv lock --keep-outdated --requirements > requirements.txt

# use pip for docker to generate the list of requirements.
RUN pip install -r requirements.txt

WORKDIR /app/hux-unified/api/huxunify
CMD ["flask", "run", "app.py"]
