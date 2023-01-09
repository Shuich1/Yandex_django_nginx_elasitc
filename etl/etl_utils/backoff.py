import time
from functools import wraps

from .config import get_logger

logger = get_logger(__name__)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции
    через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора
    (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    Args:
        start_sleep_time: начальное время повтора
        factor: во сколько раз нужно увеличить время ожидания
        border_sleep_time: граничное время ожидания

    Returns:
        func_wrapper: декоратор для функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    logger.exception('Error occurred. Trying again...')
                    logger.info(f'Waiting {sleep_time} seconds...')
                    time.sleep(sleep_time)

                    if sleep_time * factor < border_sleep_time:
                        sleep_time *= factor
                    else:
                        sleep_time = border_sleep_time
        return inner
    return func_wrapper
