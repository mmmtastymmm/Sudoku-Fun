FROM ubuntu:latest

SHELL ["/bin/bash", "--login", "-c"]

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    python3 \
    python3-numpy \
    python3-pygame \
    python3-pytest && \
    apt-get clean