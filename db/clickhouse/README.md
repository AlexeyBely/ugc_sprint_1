ClickHouse сконфигурирован на 2 шарда и 2 реплики

Для поднятия ClickHouse следует сделать ряд действий:

1. Запустить docker-compose
2. Зайти в контейнер шард1 реплика1 командой

$ docker exec -it clickhouse-node1 bash
$ clickhouse-client 

выполнить команды как в файле sql/shard1.ddl

3. Зайти в контейнер шард2 реплика1 командой 

$ docker exec -it clickhouse-node3 bash
$ clickhouse-client

выполнить команды как в файле sql/shard2.ddl