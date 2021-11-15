# Standup Scripts
Draft process to run when standing up a new DB.

## Assumptions
PYTHON 3.7 Is Installed

Following Mongo ENV Settings are Set
  - MONGO_DB_HOST
  - MONGO_DB_PORT
  - MONGO_DB_USERNAME
  - MONGO_DB_PASSWORD
  - MONGO_SSL_CERT_PATH

## Set up
If we are setting up from scratch,
make sure to drop all existing collections

## Instructions
Build the huxunifylib-database package first
```
git clone https://github.com/DeloitteHux/hux-unified.git
cd hux-unified/lib/huxunifylib-database
python -m pip install --upgrade pip
python -m pip install build twine
python -m pip install . -U
```

Set PYTHONPATH to the scripts
```
export "PYTHONPATH="/<realpath>/hux-unified/scripts:$PYTHONPATH""
export PYTHONPATH

```
Run the database create scripts
```
cd ../../../hux-unified/scripts/database
wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
python create_database_indexes.py
python prepopulate_database.py
```
