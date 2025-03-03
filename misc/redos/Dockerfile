FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev ncat

WORKDIR /app

COPY . /app

RUN chmod -R 555 /app

USER 1000:1000

CMD ncat -klvp 10001 -m 999999 -e ./wrapper.sh