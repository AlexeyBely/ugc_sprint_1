# Проектная работа 8 спринта

## Состав проекта

- Исследование: выбор хранилища OLAP.Для иследования выбраны хранилища ClickHouse и Vertica. Результаты представлены в каталоге research_db. По результатам тестов выбран ClickHouse
- Архетиктура AS IS и TO BE представлены в каталоге architecture, формат UML
- Сервис UGC

## Сервис UGC

### Порядок запуска

- Запустить хранилище ClickHouse. Описание в каталоге db/clickhouse
- Запустить стриминг событий Kafka. Описание в каталоге db/kafka
- Запустить docker-compose в корневом каталоге

### Описание работы

Для передачи временной метки представлен эндпоинт, в котором передается временная метка и id кинопроизведения. Id пользователе используется из jvt-tokena. Далее времменная метка передается в kafka в виде value - "временная метка", key - "user_id+user_movie".
 

Описание Openapi для сервиса UGC по адресу http://127.0.0.1/ugc/api/openapi

### Использованные технологии
    
- FastAPI
- Kafka 
- ClickHouse
- PlantUML

## Над проектом работали
- Алексей Белоглазов [@AlexeyBely](https://github.com/AlexeyBely)
- Андрей Гуляйко [@gulyayko](https://github.com/gulyayko)
