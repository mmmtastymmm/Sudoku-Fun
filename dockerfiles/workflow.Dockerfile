FROM ubuntu:latest

SHELL ["/bin/bash", "--login", "-c"]
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-numpy \
    python3-pygame \
    python3-pytest && \
    apt-get clean

RUN pip3 install pytype