#FROM python:3.8.1-alpine3.11
FROM python:3.8-slim

ENV FLASK_APP=docker-web-ui.py
ENV DOCKER_WEB_HOME=/opt/docker_web

ADD . /opt/docker_web

WORKDIR /opt/docker_web

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y gcc python3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
# RUN apk add --update gcc g++ musl-dev linux-headers python3-dev 

RUN pip install -r requirements.txt

EXPOSE 5000

RUN chmod +x start_docker.sh

# ENTRYPOINT [ "python" ]

CMD [ "/opt/docker_web/start_docker.sh" ]