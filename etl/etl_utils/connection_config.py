from contextlib import contextmanager

import psycopg2
from elasticsearch import Elasticsearch

from .config import get_logger

logger = get_logger(__name__)


@contextmanager
def pg_connection(dsn):
    """
    Контекстный менеджер для подключения к Postgres
    Args:
        dsn: словарь с параметрами подключения
    Yields:
        conn: объект подключения к Postgres
    """
    conn = psycopg2.connect(**dsn)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def es_connection(dsn):
    """
    Контекстный менеджер для подключения к Elasticsearch
    Args:
        dsn: строка с параметрами подключения
    Yields:
        conn: объект подключения к Elasticsearch
    """
    conn = Elasticsearch([dsn])
    try:
        yield conn
    finally:
        conn.close()
