import vertica_python
import logging
import logging.config

from cfg import LOGGING
from setting import connection_info


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('research_clickhouse')


sql_querys = [
    ('SELECT count(*) FROM frames', True),
    ('SELECT user_id, count(movie_id) FROM frames WHERE frame > 100 GROUP by user_id', False),
    ('SELECT movie_id, min(frame), max(frame) FROM frames GROUP by movie_id', False),
    ('SELECT count(*) FROM frames', True),
]

if __name__ == '__main__':
    connection = vertica_python.connect(**connection_info)
    cursor = connection.cursor()
    logger.info('start research')    
    for query, visible in sql_querys:
        response = []    
        try:
            cursor.execute(query)
            for row in cursor.iterate():
                response.append(row)            
        except Exception as e:
            logger.error(f'{type(e)}: {e}')
            break
        finally:
            if visible is True:
                logger.info(f'<{query}> {response}')
            else:
                logger.info(f'<{query}>')        
    logger.info('research OK')
    cursor.close()
    connection.close()




