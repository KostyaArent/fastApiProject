# Сервис вычисления суммы чисел массива

## Запуск на локальной машине
Установите докер и docker-compose

###### Запуск всего приложения одной командой
```
sh local_env_up.sh
```
###### Содержание local_env_up.sh
```
sudo docker-compose -f docker-compose.yml up --scale worker=2 --build
```

Он запускает веб-сервис и прослушивает сообщения на локальном хосте: 8001

#### Test over REST api
###### SYNC
```bash
curl -X GET \
  http://localhost:8001/sum/sync \
  -H 'content-type: application/json' \
  -d '{ "array": ["1", "2", "3", "4", null, "5", null, "-5"] }'
```
**Response**
```http
HTTP/1.1 200 OK
Content-Type: application/json
content-length: 13

{"result":10}
```
###### ASYNC
```bash
curl -X POST \
  http://localhost:8001/sum/async/create \
  -H 'content-type: application/json' \
  -d '{ "array": ["1", "2", "3", "4", null, "5", null, "-5"] }'
```
**Response**
```http
HTTP/1.1 200 OK
Content-Type: application/json
content-length: 45

{"id":"f00b3d14-810d-4ada-b95a-b425100c6c2f"}
```

И получение задачи
```bash
curl -X GET \
  http://localhost:8001/sum/check_task/f00b3d14-810d-4ada-b95a-b425100c6c2f
```
мы получаем статус задачи и по завершении она возвращает окончательный вывод API

когда задача находится в состоянии PROGRESS, мы получаем:
```
{
  "id": "954886f1-f625-4076-9851-e7b77bae1ffb",
  "status": "INPROGRESS",
  "result": null
}
```
когда задача находится в состоянии Completed, мы получаем:
```
{
  "id": "954886f1-f625-4076-9851-e7b77bae1ffb",
  "status": "SUCCESS",
  "result": 10  
}
```

когда задача находится в состоянии FAILURE, мы получаем:
```
{
  "status": "FAILURE",
  "result": {
    "exc_type": "OverflowError",
    "exc_message": [
      "Traceback (most recent call last):",
      "  File \"/celery_tasks/tasks.py\", line 14, in sum_task",
      "    result = sum(list(filter(None, array))),
      "OverflowError: math range error",
      ""
    ]
  },
  "date_done": "2023-01-15T11:34:24.179067",
  "task_id": "954886f1-f625-4076-9851-e7b77bae1ffb"
}
```