FROM python:3.8.1-alpine3.11

ENV FLASK_APP=docker-web-ui.py
ENV DOCKER_WEB_HOME=/opt/docker_web

ADD . /opt/docker_web

WORKDIR /opt/docker_web

RUN pip install -r requirements.txt

EXPOSE 5000

RUN chmod +x start_docker.sh

# ENTRYPOINT [ "python" ]

CMD [ "/opt/docker_web/start_docker.sh" ]