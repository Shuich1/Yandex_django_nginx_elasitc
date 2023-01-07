class Transformer:
    """
    Класс для трансформации данных из Postgres в ElasticSearch
    """
    def __init__(self, logger):
        self.logger = logger

    def transform(self, batch):
        """
        Функция для трансформации данных из Postgres в ElasticSearch
        """
        transformed_batch = []
        try:
            for row in batch:
                writers = []
                actors = []
                director = []
                writers_names = []
                actors_names = []

                for person in row[7]:
                    if person['person_role'] == 'director':
                        director = person['person_name']
                    elif person['person_role'] == 'writer':
                        writers_names.append(person['person_name'])
                        writers.append(
                            {
                                'id': person['person_id'],
                                'name': person['person_name']
                            }
                        )
                    elif person['person_role'] == 'actor':
                        actors_names.append(person['person_name'])
                        actors.append(
                            {
                                'id': person['person_id'],
                                'name': person['person_name']
                            }
                        )

                transformed_batch.append({
                    '_index': 'movies',
                    '_type': '_doc',
                    '_id': row[0],
                    '_source': {
                        'id': row[0],
                        'imdb_rating': row[3],
                        'genre': row[8],
                        'title': row[1],
                        'description': row[2],
                        'director': director,
                        'actors_names': actors_names,
                        'writers_names': writers_names,
                        'actors': actors,
                        'writers': writers
                    }
                })
        except Exception:
            self.logger.exception('Error while transforming batch')
        return transformed_batch
