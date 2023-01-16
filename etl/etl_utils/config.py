import logging
import logging.config
import time
import os

from pydantic import BaseModel, BaseSettings, Field


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
    if not os.path.exists('logs'):
        os.mkdir('logs')

    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)


class ESIndexConfig(BaseModel):
    settings = {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "russian_stop": {
                    "type":       "stop",
                    "stopwords":  "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer"
                    ]
                }
            }
        }
    }

    mappings = {
        "dynamic": "strict",
        "properties": {
            "id": {
                "type": "keyword"
            },
            "imdb_rating": {
                "type": "float"
            },
            "genre": {
                "type": "keyword"
            },
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {
                    "raw": {
                        "type":  "keyword"
                    }
                }
            },
            "description": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "director": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "actors_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "writers_names": {
                "type": "text",
                "analyzer": "ru_en"
            },
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                    }
                }
            }
        }
    }

    index_name = 'movies'


class PostgresConfig(BaseSettings):
    dbname: str = Field('movies_database', env='POSTGRES_DB')
    user: str = Field('app', env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field('db', env='POSTGRES_HOST')
    port: str = Field(5432, env='POSTGRES_PORT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ElasticConfig(BaseSettings):
    host: str = Field('elastic', env='ELASTIC_HOST')
    port: str = Field(9200, env='ELASTIC_PORT')

    def get_url(self):
        return f'http://{self.host}:{self.port}'


class ETLServicesConfig(BaseSettings):
    postgres: dict = PostgresConfig().dict()
    elastic: str = ElasticConfig().get_url()
    index_config: ESIndexConfig = ESIndexConfig()
    sleep_time: int = Field(60, env='SLEEP_TIME')
    batch_size: int = Field(100, env='BATCH_SIZE')
