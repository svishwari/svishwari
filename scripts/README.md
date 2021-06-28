# scripts
Purpose of this directory is for housing scripts for initializing the database required for the project.

# Steps to run Scripts
```
cd /scripts
pipenv install
pipenv shell

cd /database
pipenv run create_database_indexes.py
pipenv run prepopulate_database.py
pipenv run set_database_constants.py
```
