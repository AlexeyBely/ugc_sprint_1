Для поднятия Kafka следует сделать ряд действий:

1. Запустить docker-compose \n
2. Дождаться запуска kafka, проверить Confluent по адресу http://localhost:9021 \n
3. Зайти в контейнер broker \n
    $docker exec -it broker bash \n
    $kafka-topics --create --topic movies-frames --bootstrap-server localhost:9092