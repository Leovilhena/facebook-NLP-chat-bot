FROM python:3.7.0-slim
LABEL maintainer="leosvilhena@icloud.com"

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV HOST '127.0.0.1'
ENV PORT 443

RUN mkdir webserver
WORKDIR /webserver

COPY requirements.txt ./
COPY webserver.py ./
COPY apps ./apps

RUN set -ex \
    && apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends \
        python-pip \
        python-dev \
        build-essential \
        apt-utils \
    && pip install -r requirements.txt \
    && apt-get purge --auto-remove -yqq python-dev \
    && apt-get purge --auto-remove -yqq build-essential \
    && apt-get clean

RUN chmod u+x ./webserver.py

EXPOSE 443

ENTRYPOINT ["python3.7", "webserver.py"]