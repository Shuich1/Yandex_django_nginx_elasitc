import datetime
import logging
import time

from etl_process.elasticsearch_loader import ElasticsearchLoader
from etl_process.postgres_extractor import PostgresExtractor
from etl_process.transformer import Transformer
from etl_utils.backoff import backoff
from etl_utils.config import ETLServicesConfig, get_logger
from etl_utils.state_storage import JsonFileStorage, State


@backoff()
def etl_process(
    extractor: PostgresExtractor,
    transformer: Transformer,
    loader: ElasticsearchLoader,
    state: State,
    logger: logging.Logger
):
    """
    Функция для запуска ETL процесса для
    загрузки данных из Postgres в ElasticSearch
    """
    logger.info('ETL process started')

    last_etl_process_time = state.get_state('last_etl_process_time')
    logger.info(f'Last ETL process time: {last_etl_process_time}')

    for i, batch in enumerate(extractor.extract(last_etl_process_time)):
        logger.info(f'Extracted {i+1} batch')
        transformed_batch = transformer.transform(batch)
        logger.info(f'Transformed {i+1} batch')
        loader.load(transformed_batch)
        logger.info(f'Loaded {i+1} batch')

    state.set_state(
        'last_etl_process_time',
        datetime.datetime.now().isoformat()
    )

    logger.info(
        f'This ETL process time:'
        f'{state.get_state("last_etl_process_time")}'
    )

    logger.info('ETL process finished')

    state.set_state('previous_extracted_ids', [])


if __name__ == '__main__':
    config = ETLServicesConfig()
    logger = get_logger(__name__)

    state = State(JsonFileStorage('state.json'))

    pg_dsn = config.postgres
    es_dsn = config.elastic
    batch_size = config.batch_size

    extractor = PostgresExtractor(pg_dsn, batch_size, state, logger)
    transformer = Transformer(logger)
    loader = ElasticsearchLoader(es_dsn, logger)

    sleep_time = config.sleep_time

    while True:
        etl_process(extractor, transformer, loader, state, logger)
        logger.info(f'Waiting {sleep_time} seconds before next ETL process')
        time.sleep(sleep_time)
