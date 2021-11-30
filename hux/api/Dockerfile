# 1. Build the API

FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

# variables used for consuming orchestration pkgs from jfrog
ARG ARTIFACTORY_PYTHON_READ

# set the work dir on the docker image
WORKDIR /app/hux-unified/api

# copy over the hux/api folder from the host to the container
COPY ./hux/api /app/hux-unified/api
COPY ./lib /app/lib
COPY .pylintrc /app
COPY .coveragerc /app

# upgrade pip to the latest
RUN pip install pip --upgrade

# install pipenv
RUN pip install pipenv --upgrade

# workaround for setuptools because of fuelSDK suds-jurko.
RUN pip install setuptools==56.1.0

# lock current deps to make it easier/faster for docker to build
RUN pipenv install --system --deploy

# set the working directory again
WORKDIR /app/hux-unified/api

# append huxunify path to python path.
ENV PYTHONPATH "${PYTHONPATH}:/app/hux-unified/api"

# set to dev
ENV FLASK_ENV=development
ENV AWS_REGION=us-east-1
ENV DEBUG_METRICS=True

# run the python application
EXPOSE 80
EXPOSE 8080
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["huxunify/app.py"]
