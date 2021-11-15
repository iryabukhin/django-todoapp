FROM python:3.9

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PROJECT_ROOT=/usr/src/app

RUN mkdir -pv $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

COPY ./requirements.txt $PROJECT_ROOT/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app