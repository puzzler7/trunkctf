FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

RUN pip3 install flask Flask-Limiter

COPY . /app

RUN chmod -R 777 /app

USER 1000:1000

ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]