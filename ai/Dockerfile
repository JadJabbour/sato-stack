FROM tensorflow/tensorflow:latest-gpu

WORKDIR /ai

RUN apt-get update -y

RUN apt-get install -y python3.8

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

RUN apt-get install -y graphviz

COPY Pipfile Pipfile

COPY Pipfile.lock Pipfile.lock

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install pipenv && python3 -m pipenv install --ignore-pipfile

COPY ./docker-config.ini ./config.ini

COPY . .