import logging

from elasticsearch.helpers import bulk
from etl_utils.backoff import backoff
from etl_utils.config import ETLServicesConfig
from etl_utils.connection_config import es_connection


class ElasticsearchLoader:
    def __init__(self, dsn: dict, logger: logging.Logger) -> None:
        self.dsn = dsn
        self.logger = logger
        self.create_index()

    @backoff()
    def create_index(self):
        with es_connection(self.dsn) as es:
            if not es.ping():
                raise Exception(
                    'Elasticsearch is not available, '
                    'maybe it is still starting up?'
                )

            if not es.indices.exists(index='movies'):
                es.indices.create(
                    index=ETLServicesConfig().index_config.index_name,
                    settings=ETLServicesConfig().index_config.settings,
                    mappings=ETLServicesConfig().index_config.mappings
                )
                self.logger.info('Index movies created')

    @backoff()
    def load(self, transformed_batch: list[dict]):
        """
        Загрузка данных в Elasticsearch
        Args:
            transformed_batch: список словарей с данными
        Returns:
            список id загруженных документов
        """
        with es_connection(self.dsn) as es:
            if not es.ping():
                raise Exception('Elasticsearch is not available')
            bulk(es, transformed_batch)
