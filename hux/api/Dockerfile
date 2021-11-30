# 1. Build dependencies image -----------------
FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS python-dependencies

ARG ARTIFACTORY_PYTHON_READ

# Set working dir
WORKDIR /app/hux-unified/api

# Copy over repo files
COPY ./hux/api /app/hux-unified/api
COPY ./lib /app/lib
COPY .pylintrc /app
COPY .coveragerc /app

# upgrade pip to the latest
RUN pip install pip --upgrade

# install pipenv
RUN pip install pipenv --upgrade

# lock current deps to make it easier/faster for docker to build
RUN pipenv install --system --deploy

# set the working directory again
WORKDIR /app/hux-unified/api

# 2. Build the API -----------------

FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

# Copy app over to image
COPY --from=python-dependencies /app /app
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
