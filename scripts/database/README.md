# Standup Scripts
Draft of process to run when standing up a new DB.

## Assumptions
Following Mongo ENV Settings are Set
  - MONGO_DB_HOST
  - MONGO_DB_PORT
  - MONGO_DB_USERNAME
  - MONGO_DB_PASSWORD
  - MONGO_SSL_CERT_PATH

## Instructions
Build the huxunifylib-database package first
```
git clone https://github.com/DeloitteHux/hux-unified.git
cd hux-unified/lib/huxunifylib-database
python -m pip install --upgrade pip
python -m pip install build twine
rm -rf ./dist
python -m build -s -w . --outdir ./dist
python -m pip install .
```

Run the database create scripts
```
cd ../../../hux-unified/scripts/database
python create_database_indexes.py
python set_database_constants.py
pytest mongo_db_test.py
```