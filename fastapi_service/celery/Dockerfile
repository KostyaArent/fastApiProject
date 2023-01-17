FROM tiangolo/uvicorn-gunicorn:python3.10

LABEL maintainer="KATrepalin <katrepalin@yandex.ru>"

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./. /celery_tasks
WORKDIR /celery_tasks

ENTRYPOINT celery -A tasks worker --loglevel=info