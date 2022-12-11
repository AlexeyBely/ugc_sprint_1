# Иследование на выбор ClickHouse или Vertica

Подготовка хранилища ClickHouse описана в db/clickhouse, Vertica при запуске docker-compose.   
Время выполнения запросов сохраняется в лог файл (log/logfile.log)   

Результат:  

10000000 записей:    
ClickHouse - 957,5 с   
Vertica - 977,5 с   
   
Среднее время на 1000 записей:   
ClickHouse - 95,8 мс   
Vertica - 97,8 мс   
   
Запрос на количество записей (сред. время за 3 запроса):   
<SELECT count() FROM movies.frames>   
ClickHouse - 10 мс   
Vertica - 30 мс   

Запрос вида (сред. время за 3 запроса):   
<SELECT user_id, uniq(movie_id) FROM movies.frames WHERE frame > 100 GROUP by user_id>   
ClickHouse - 1332 мс   
Vertica - 1538 мс   

Запрос вида (сред. время за 3 запроса):   
<SELECT movie_id, min(frame), max(frame) FROM movies.frames GROUP by movie_id>   
ClickHouse - 467 мс   
Vertica - 1321 мс   


Вывод:   
Время записи по 1000 строк, практически, одинаковое. Запросы на чтение ClickHouse отрабатывает значительно быстрее.   
Для хранилища OLAP выбран ClickHouse.    



