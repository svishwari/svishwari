FROM huxhub.repo.mgnt.in/python:3.7-slim-buster AS hux-unified

# set the work dir on the docker image
WORKDIR /app/hux-unified/load_tests/api

COPY . /app/hux-unified/load_tests/api

RUN pip install python-dotenv
RUN pip install locust
RUN pip install pyperclip

CMD ["locust",
        "--locustfile", "/app/hux-unified/load_tests/api/locustfile.py", \
        "--headless", \
        "--users", "2", \
        "--spawn-rate", "20", \
        "--run-time", "200", \
        "--html", "load_test_report.html"]
