# 1. Build the API

#FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified
FROM python:3.7-slim-buster AS hux-unified

# variables used for consuming orchestration pkgs from jfrog
ARG ARTIFACTORY_PYTHON_READ

# set the work dir on the docker image
WORKDIR /app/hux-unified/api

# copy over the hux/api folder from the host to the container
COPY ./hux/api /app/hux-unified/api

# upgrade pip to the latest
RUN pip install --upgrade pip

# install pipenv
RUN pip install pipenv

# lock current deps to make it easier/faster for docker to build
RUN pipenv lock --keep-outdated --requirements > requirements.txt

# use pip for docker to generate the list of requirements.
RUN pip install -r requirements.txt

# TODO - this was the only way I could fix it.
# need to show for demo, can revisit after.
RUN pip uninstall bson -y
RUN pip uninstall pymongo -y
RUN pip install bson
RUN pip install pymongo

# set the working directory again
WORKDIR /app/hux-unified/api

# append huxunify path to python path.
ENV PYTHONPATH "${PYTHONPATH}:/app/hux-unified/api"

# run the python application
EXPOSE 80
EXPOSE 8080
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["huxunify/app.py"]
