### Running PyTest tests

### Pre-requisites

Run the below command to install tavern package
```buildoutcfg
# cd to this folder
pip install pip -U
pip install pytest
pip install pymongo
pip install requests
```

### Running the integration tests

The below environment variables has to be set as the as part of the pytest run configuration.

#### Environment variables to be set
```buildoutcfg
FLASK_ENV=pytest
OKTA_ISSUER=https://deloittedigital-ms.okta.com
OKTA_CLIENT_ID=0oab1i3ldgYyRvk5r2p7
OKTA_REDIRECT_URI=https://unified-ui-dev.main.use1.hux-unified-dev1.in/login/callback
OKTA_TEST_USER_NAME=unified-dev-test-user@deloitte.com
OKTA_TEST_USER_PW=<OKTA_TEST_USER_NAME_PASSWORD_VALUE> # Can be found in 1password for unified-dev-test-user@deloitte.com user
MONGO_DB_HOST=<MONGO_DB_HOST_OF_TEST_ENV>
MONGO_DB_PORT=27017
MONGO_DB_USERNAME=read_write_user
MONGO_DB_PASSWORD=<MONGO_DB_PASSWORD_VALUE> # Can be found in 1password against the Mongo username of corresponding Mongo host
INT_TEST_HOST=<INT_TEST_HOST_URL> # For instance, https://unified-api-dev.main.use1.hux-unified-dev1.in for DEV1
INT_TEST_API_VERSION=api/v1 # API version of the backend API application
```

Once the above env variables are set on the appropriate run configuration of the integration test set up to run using pytest as the runner,
then any test file in ./test folder/dir can be run to execute the tests in that test file.

Alternatively, the below command can be executed in current folder/dir to run all tests in the <TEST_FILE_NAME> file.
```buildoutcfg
# run pytest
py.test test/<TEST_FILE_NAME> -v
```

If following the above alternate way to run the tests using `py.test` on CLI, then all the environment variables need to be set up using
`export`(for Mac) or `set`(for Windows) command to set the required environment variables before running the `py.test` command to run.<br>
Any special characters(like ;, $, -, {, ~, *, &) in these environment variable values has to be escaped using a `\`(backslash) character
when exporting or setting them in the current CLI session as env variables.<br>
<br>
**NOTE** that these environment variables will be set and hold true **ONLY** in that terminal session these commands were run on.

### Sample Output

Following is the sample output of running an integration test script using pytest.

When run via a run configuration from an IDE.
```buildoutcfg
Launching pytest with arguments <ABS_PATH_TO_hux-unified>/hux-unified/hux/integration_tests/api/test/test_client_project.py --no-header --no-summary -q in <ABS_PATH_TO_hux-unified>/hux-unified/hux/integration_tests/api/test

============================= test session starts ==============================
collecting ... collected 2 items

test_client_project.py::TestClientProjects::test_get_client_projects
test_client_project.py::TestClientProjects::test_patch_client_projects

============================== 2 passed in 1.40s ===============================

Process finished with exit code 0
PASSED [ 50%]PASSED [100%]
```

When run via command line using `py.test` command.
```buildoutcfg
=========================================================================== test session starts ===========================================================================
platform darwin -- Python 3.7.9, pytest-6.2.5, py-1.10.0, pluggy-1.0.0 -- /Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7
cachedir: .pytest_cache
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('<ABS_PATH_TO_hux-unified>/hux-unified/hux/integration_tests/api/.hypothesis/examples')
rootdir: <ABS_PATH_TO_hux-unified>/hux-unified/hux/integration_tests/api, configfile: pytest.ini
plugins: requests-mock-1.9.3, hypothesis-6.23.2, tavern-1.16.2
collected 2 items

test/test_client_project.py::TestClientProjects::test_get_client_projects PASSED                                                                                    [ 50%]
test/test_client_project.py::TestClientProjects::test_patch_client_projects PASSED                                                                                  [100%]

============================================================================ 2 passed in 1.34s ============================================================================
```
