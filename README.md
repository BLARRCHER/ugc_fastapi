/ugc - cервис UGC на FastAPI  
/etl - ETL сервис  
/docs - Диаграммы по проекту  
/research - Исследование по 2 бд: Clickhouse, Vertica


Команды
- `make format` отформатировать код
- `make lint` запустить линтер (flake8)
- `make run` запустить сервисы
- `make stop` остановить сервисы
- `make etl-logs` посмотреть логи etl
- `make build-all`: собрать образы
- `prod-run`: запустить production версию


Запустить проект: 
- создать .env в ./ (достаточно скопировать из ./.env.example)
- `make run`


Тесты:

- Тесты API `pytest ugc/tests` (предварительно установить зависимости из ugc/requirements.txt, ugc/requirements.dev.txt)
- Тесты ETL `pytest etl/tests` (предварительно установить зависимости из etl/requirements.txt, etl/requirements.dev.txt)
