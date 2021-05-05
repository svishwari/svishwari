# 1. Build the API

FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

# variables used for consuming orchestration pkgs from jfrog
ARG ARTIFACTORY_PYTHON_READ

WORKDIR /app/hux-unified/api
COPY ./lib /app/lib
COPY ./hux/api /app/hux-unified/api
COPY .pylintrc /app

# install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# pipenv sync to ensure pipenv pkgs are aligned with pipfile.lock
RUN pipenv sync

# generate requirements.txt for the pipefile env
RUN pipenv run pip freeze > requirements.txt

# use pip for docker to generate the list of requirements.
RUN pip install -r requirements.txt

WORKDIR /app/hux-unified/api/huxunify
CMD ["pipenv", "run", "app.py"]
