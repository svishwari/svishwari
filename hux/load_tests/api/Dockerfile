FROM locustio/locust

WORKDIR /app/hux-unified/load_tests

COPY ./load_tests /app/hux-unified/load_tests

RUN pip install python-dotenv
RUN pip install locust
RUN pip install pyperclip

CMD ["--locustfile", "/app/hux-unified/load_tests/locustfile.py", \
        "--headless", \
        "--users", "2", \
        "--spawn-rate", "20", \
        "--run-time", "200", \
        "--html", "load_test_report.html"]
