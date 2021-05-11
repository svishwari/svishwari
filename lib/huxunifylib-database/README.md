# huxunifylib-database
[![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/deloittehux/Hux_Unified_Solution%2Funified_solution_library?type=cf-1&key=eyJhbGciOiJIUzI1NiJ9.NWRjMzBjMmJiMGVmMzJiNzkxM2Y2MGJh.GkhczDGoVzfrLnhTAn2b9yqwMQkP_wXNMhwGDPRPStQ)]( https://g.codefresh.io/pipelines/edit/new/builds?id=606bf0961ca52d74786e76ef&pipeline=unified_solution_library&projects=Hux_Unified_Solution&projectId=605a4546bfffd0aea1e243a0)

huxunifylib-database is a library for managing the huxunify database.

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
