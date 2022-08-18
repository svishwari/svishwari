FROM themattrix/tox-base

RUN apt-get update && apt-get -y upgrade && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN curl -0s https://uploader.codecov.io/v0.2.5/linux/codecov -o codecov
RUN chmod +x codecov

RUN cp codecov ../usr/local/bin/

ONBUILD COPY install-prereqs*.sh requirements*.txt tox.ini /app/
ONBUILD ARG SKIP_TOX=false
ONBUILD RUN bash -c " \
 if [ -f '/app/install-prereqs.sh' ]; then \
     bash /app/install-prereqs.sh; \
 fi && \
 if [ $SKIP_TOX == false ]; then \
     TOXBUILD=true tox; \
 fi
