## Приложение
Запуск: `uvicorn src.main:app`

## RabbitMQ
Запуск: `sudo systemctl start rabbitmq-server`

Состояние очередей: `sudo rabbitmqctl list_queues`

## Celery
Запуск: `celery -A src worker`

## Tests
Запуск: `pytest .\tests\auth\test_dependencies.py::test_check_not_exists -s`
`-s` для захвата вывода.