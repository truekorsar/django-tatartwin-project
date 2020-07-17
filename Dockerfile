FROM ubuntu:latest

RUN  apt-get -y update\
    && apt-get -y install python3.8 gcc python3.8-dev python3-setuptools python3-pip

WORKDIR /usr/local/src/project

COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["bash", "/usr/local/src/project/docker-setup-project/web/init-project.sh"]
