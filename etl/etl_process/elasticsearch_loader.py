from etl_utils.connection_config import es_connection
from elasticsearch.helpers import bulk
from etl_utils.index_settings import settings, mappings
from etl_utils.backoff import backoff


class ElasticsearchLoader:
    def __init__(self, dsn, logger):
        self.dsn = dsn
        self.logger = logger
        self.create_index()

    @backoff()
    def create_index(self):
        with es_connection(self.dsn) as es:
            if not es.indices.exists(index='movies'):
                es.indices.create(
                    index='movies',
                    settings=settings,
                    mappings=mappings
                )
                self.logger.info('Index movies created')

    @backoff()
    def load(self, transformed_batch) -> list:
        """
        Загрузка данных в Elasticsearch
        Args:
            transformed_batch: список словарей с данными
        Returns:
            список id загруженных документов
        """
        self.logger.info(self.dsn)
        with es_connection(self.dsn) as es:
            bulk(es, transformed_batch)
        return [doc['_id'] for doc in transformed_batch]
