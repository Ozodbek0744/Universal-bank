FROM python:3.9.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --upgrade pip && pip install -r requirements.txt