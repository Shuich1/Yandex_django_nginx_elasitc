Django + Nginx + PostgreSQL + ElasticSearch + Docker Compose Web App
===============================================
This is a Django web app that uses Docker Compose to run a Django app with a PostgreSQL database and Nginx web server with sync with ElasticSearch.

## Requirements
- Docker
- Docker Compose

## Installation
1. Clone the repository `git clone https://github.com/Shuich1/new_admin_panel_sprint_2.git`
2. Create .env file in the `root directory` and `etl directory` with template from example.env
3. Run `mkdir esdata && chown 1000:1000 esdata` in the root directory to create and set permissions for ElasticSearch data directory
4. Run `docker-compose up` in the root directory to build the images and run the containers
5. Run `docker-compose run -v $(pwd)/sqlite_to_postgres:/sqlite_to_postgres -w /sqlite_to_postgres --entrypoint="/bin/bash -c" backend "python load_data.py"` in the root directory to load data from sqlite to postgres
6. Run `docker-compose run --entrypoint="/bin/bash -c" backend "python manage.py createsuperuser"` in the root directory to create superuser

## Usage
- The Django admin will be available at http://127.0.0.1:8000/admin
- The Django API will be available at http://127.0.0.1:8000/api/v1/movies and http://127.0.0.1:8000/api/v1/movies/{id}
