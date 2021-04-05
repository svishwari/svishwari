# hux-unified lib

# todo - update codefresh link
[![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/deloittehux/advertising_performance%2Fdatabase?type=cf-1&key=eyJhbGciOiJIUzI1NiJ9.NWRjMzBjMmJiMGVmMzJiNzkxM2Y2MGJh.GkhczDGoVzfrLnhTAn2b9yqwMQkP_wXNMhwGDPRPStQ)]( https://g.codefresh.io/pipelines/edit/new/builds?id=5f3d2ac0acded2bc696a7e10&pipeline=database&projects=advertising_performance&projectId=5f3c2c985ed18a34eb76775a)

The `huxunifylib` houses all huxunified python libs used.

## Usage

Refer to the examples in this section for initializing a database client.

### Connecting to a Single mongod Server

```python
from huxunifylib.database.client import DatabaseClient

# intialize a database client with the appropriate user credentials
client = DatabaseClient("localhost", 27017, "myUserName", "myPassword")

# connect to the database
db = client.connect()

# if a database client was initialized
if db:

    # print a message
    print("Database client initialized successfully on localhost:27017 with "
        f"username {db.username}.")

# else if the database client wasn't initialized
else:

    # print a message
    print("Database client could not be initialized on localhost:27017 "
        "with username myUserName.")
```

### Connecting to a Replica Set

```python
from huxunifylib.database.client import DatabaseClient

# set up the list of replica set hosts
hosts = ["replicasetmember1", "replicasetmember2"]

# intialize a database client with the appropriate user credentials
client = DatabaseClient(hosts, 27017, "myUserName", "myPassword")

# connect to the database
db = client.connect()

# if a database client was initialized
if db:

    # print a message
    print("Database client initialized successfully for requested "
        f"replica set with username {db.username}.")

# else if the database client wasn't initialized
else:

    # print a message
    print("Database client could not be initialized for requested "
        "replica set with username myUserName.")
```
