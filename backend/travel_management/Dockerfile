FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install pipenv

RUN pipenv install --ignore-pipfile

EXPOSE 8000