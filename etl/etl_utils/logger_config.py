import logging
import logging.config
import time

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S'
        },
    },
    'handlers': {
        'log_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': f'logs/{time.strftime("%Y-%m-%d %H:%M:%S")}.log',
            'formatter': 'default',
        },
     },
    'loggers': {
        '': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': True
        },
     },
}


def get_logger(name: str) -> logging.Logger:
    """
    Функция для получения логгера
    Args:
        name: имя логгера
    Returns:
        logger: логгер
    """
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)
