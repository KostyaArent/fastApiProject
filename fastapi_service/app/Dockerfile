FROM tiangolo/uvicorn-gunicorn:python3.10

LABEL maintainer="KATrepalin <katrepalin@yandex.ru>"

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./. /app
WORKDIR /app
