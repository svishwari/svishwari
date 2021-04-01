# 1. Build the API

FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS unified-api

MAINTAINER Jim McMahon <jimcmahon@deloitte.com>

# Setup virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app/unified_api/api
COPY ./huxunify/api /app/unified_api/api

# TODO how should pip install work here?
RUN pip-env Pipfile
# Can we use the pipfile somehow or do we need to use req.txt as seen in ad perf repo?

# TODO what should the run command look like here?
CMD ["pipenv", "python3", "app.py"]