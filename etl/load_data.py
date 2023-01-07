import time
import datetime
import os
from dotenv import load_dotenv
from etl_utils.backoff import backoff
from etl_utils.logger_config import get_logger
from etl_utils.state_storage import State, JsonFileStorage
from etl_process.postgres_extractor import PostgresExtractor
from etl_process.transformer import Transformer
from etl_process.elasticsearch_loader import ElasticsearchLoader


@backoff()
def etl_process(extractor, transformer, loader, state, loaded_before_error_ids, logger):
    """
    Функция для запуска ETL процесса для
    загрузки данных из Postgres в ElasticSearch
    """
    logger.info('ETL process started')

    last_etl_process_time = state.get_state('last_etl_process_time')
    logger.info(f'Last ETL process time: {last_etl_process_time}')

    try:
        for i, batch in enumerate(extractor.extract(last_etl_process_time)):
            logger.info(f'Extracted {i+1} batch')
            transformed_batch = transformer.transform(batch)
            logger.info(f'Transformed {i+1} batch')
            loaded_ids_in_batch = loader.load(transformed_batch)
            loaded_before_error_ids.extend(loaded_ids_in_batch)
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

    except Exception:
        state.set_state(
            'loaded_before_error_ids',
            loaded_before_error_ids
        )
        logger.exception('ETL process failed')
        return


if __name__ == '__main__':
    load_dotenv()

    logger = get_logger(__name__)

    state = State(JsonFileStorage('state.json'))

    pg_dsn = {
        'dbname': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('POSTGRES_HOST'),
        'port': os.environ.get('POSTGRES_PORT')
    }

    es_dsn = os.environ.get('ES_DSN')

    extractor = PostgresExtractor(pg_dsn, 100, state, logger)
    transformer = Transformer(logger)
    loader = ElasticsearchLoader(es_dsn, logger)

    sleep_time = int(os.environ.get('SLEEP_TIME'))

    while True:
        loaded_before_error_ids = []
        etl_process(extractor, transformer, loader, state, loaded_before_error_ids, logger)
        logger.info(f'Waiting {sleep_time} seconds before next ETL process')
        time.sleep(sleep_time)
