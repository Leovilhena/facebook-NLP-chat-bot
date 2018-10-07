FROM python:3.7.0-slim
LABEL maintainer="leosvilhena@icloud.com"

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
ENV HOST '127.0.0.1'
ENV PORT 8080