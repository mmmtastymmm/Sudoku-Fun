FROM ubuntu:impish

SHELL ["/bin/bash", "--login", "-c"]
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-numpy \
    python3-pygame && \
    apt-get clean

ADD . /app

WORKDIR /app

ENTRYPOINT ["python3", "main.py"]