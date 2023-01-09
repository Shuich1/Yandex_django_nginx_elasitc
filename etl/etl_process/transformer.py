class Transformer:
    """
    Класс для трансформации данных из Postgres в ElasticSearch
    """
    def __init__(self) -> None:
        pass

    def transform(self, batch: dict) -> list[dict]:
        """
        Функция для трансформации данных из Postgres в ElasticSearch
        """
        transformed_batch = []
        for row in batch:
            writers = []
            actors = []
            director = []
            writers_names = []
            actors_names = []

            for person in row['persons']:
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
                '_id': row['id'],
                '_source': {
                    'id': row['id'],
                    'imdb_rating': row['rating'],
                    'genre': row['genres'],
                    'title': row['title'],
                    'description': row['description'],
                    'director': director,
                    'actors_names': actors_names,
                    'writers_names': writers_names,
                    'actors': actors,
                    'writers': writers
                }
            })
        return transformed_batch
