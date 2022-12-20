from functools import wraps
from time import sleep
import logging.config

from config.cfg import LOGGING

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


def backoff(
        start_sleep_time: float = 0.1,
        factor: int = 2,
        border_sleep_time: float = 10.0,
        retries_with_max_timeout: int = 5,
        logger=LOGGER,

):
    """
    Rerun wrapped function after some time in case of error.
    Rerun time exponentially (factor) increases up to max time (border_sleep_time)
    :logger: LOGGER object
    :start_sleep_time: start rerun time
    :factor: increase sleep time in <factor> times
    :border_sleep_time: max rerun time
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            n = 0
            flag = True
            while flag:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(e)
                    max_timeout_attempts = 0
                    sleep_time = start_sleep_time * factor ** n if sleep_time < border_sleep_time else border_sleep_time
                    LOGGER.info(f'Next attempt in {sleep_time} second')
                    sleep(sleep_time)
                    n += 1
                    if sleep_time == border_sleep_time:
                        max_timeout_attempts += 1
                        if max_timeout_attempts > retries_with_max_timeout:
                            logger.error('max number of connection attempts has reached, quit')
                            flag = False
        return inner
    return func_wrapper
