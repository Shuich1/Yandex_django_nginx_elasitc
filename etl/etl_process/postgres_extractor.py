import datetime
from etl_utils.connection_config import pg_connection


class PostgresExtractor:
    """Извлекает данные из Postgres"""
    def __init__(self, pg_dsn, batch_size: int, state, logger):
        self.batch_size = batch_size
        self.state = state
        self.logger = logger
        self.pg_dsn = pg_dsn

    def extract(self, last_etl_process_time: datetime.datetime):
        """Извлекает данные из Postgres"""
        with pg_connection(self.pg_dsn) as conn:
            with conn.cursor() as cursor:
                query = f"""
                    SELECT
                        fw.id,
                        fw.title,
                        fw.description,
                        fw.rating,
                        fw.type,
                        fw.created,
                        fw.modified,
                        COALESCE (
                            json_agg(
                                DISTINCT jsonb_build_object(
                                    'person_role', pfw.role,
                                    'person_id', p.id,
                                    'person_name', p.full_name
                                )
                            ) FILTER (WHERE p.id is not null),
                            '[]'
                        ) as persons,
                        array_agg(DISTINCT g.name) as genres
                        FROM content.film_work fw
                        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                        LEFT JOIN content.person p ON p.id = pfw.person_id
                        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                        LEFT JOIN content.genre g ON g.id = gfw.genre_id
                        GROUP BY fw.id
                        HAVING GREATEST(fw.modified, MAX(p.modified), MAX(g.modified)) > '{last_etl_process_time}'
                    """
                loaded_before_error_ids = tuple(self.state.get_state('loaded_before_error_ids'))
                if loaded_before_error_ids:
                    query += f'AND fw.id NOT IN {loaded_before_error_ids} '
                    query += 'ORDER BY GREATEST(fw.modified, MAX(p.modified), MAX(g.modified));'

                cursor.execute(query)

                while True:
                    batch = cursor.fetchmany(self.batch_size)
                    if not batch:
                        break
                    self.logger.info(f'Extracted {len(batch)} rows from Postgres')
                    yield batch
