Для поднятия Kafka следует сделать ряд действий:

1. Запустить docker-compose --env-file ./db/kafka/.env up -d    
2. Дождаться запуска kafka, проверить Confluent по адресу http://localhost:9021  
3. Зайти в контейнер broker  
    $docker exec -it broker bash  
4. Создать топик movies-frames     
    $kafka-topics --create --topic movies-frames --bootstrap-server localhost:9092