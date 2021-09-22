Purpose of this folder is to house all the integration tests for the API and UI.

### Running tavern tests

### Pre-requisites

Run the below command to install tavern package
```buildoutcfg
# cd to this folder
pip install pip -U
pip install tavern
```

Run the following commands in a terminal session depending on the OS type as shown below to set up the test hostname and api version the tests need to be run against.

For instance:
<hostname_of_test_server> can be set to http://localhost:<port_no> or https://unified-api-dev.main.use1.hux-unified-dev1.in for DEV1 depending on which env the tests neeed to be run against.
<api_version> can be set to api/v1

#### Windows
```buildoutcfg
SET TAVERN_TEST_HOST=https://<hostname_of_test_server>
SET TAVERN_TEST_API_VERSION=<api_version>
```
To validate if the env variables is set as needed after running the above commands.
```buildoutcfg
echo %TAVERN_TEST_HOST%
echo %TAVERN_TEST_API_VERSION%
```
#### Mac/Linux
```buildoutcfg
TAVERN_TEST_HOST=https://<hostname_of_test_server>
TAVERN_TEST_API_VERSION=<api_version>
```
To validate if the env variables is set as needed after running the above commands.
```buildoutcfg
echo $TAVERN_TEST_HOST
echo $TAVERN_TEST_API_VERSION
```

**NOTE** that these environment variables will be set and hold true **ONLY** in that terminal session these commands were run on.

Make sure the below variable in \hux-unified\hux\integration_tests\api\common.yaml file is set with appropriate value.
```yaml
token: <okta_access_token_value> (for instance: personal okta access token to access HUX UI)
```

Run the below command in this folder/dir to run all tavern tests.
```buildoutcfg
# run pytest
py.test -v
```

### Sample Output

Following is the sample output of running a simple health check tavern test.
```buildoutcfg
============================================================================ test session starts ============================================================================
platform darwin -- Python 3.7.9, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /Users/douglaslong/Documents/repos/hux-unified/hux/integration_tests
plugins: tavern-1.16.0, hypothesis-6.14.2, requests-mock-1.9.3, Faker-8.10.1, typeguard-2.12.0
collected 1 item

api/test_core.tavern.yaml .                                                                                                                                           [100%]

============================================================================= 1 passed in 0.62s =============================================================================
```

### Calling External Functions for Complex Validations
Tavern supports access to external functions in a python script as long as the script is part of PYTHONPATH environment variable when executing the test.

PYTHONPATH environment variable can be set in a terminal session depending on the OS type as shown below.

#### Windows
```buildoutcfg
SET PYTHONPATH=%PYTHONPATH%;<absolute_path_to_script>
```
To validate if the PYTHONPATH env variable is set accordingly after running the above command.
```buildoutcfg
echo %PYTHONPATH%
```
#### Mac/Linux
```buildoutcfg
PYTHONPATH=$PYTHONPATH:<absolute_path_to_script>
```
To validate if the PYTHONPATH env variable is set accordingly after running the above command.
```buildoutcfg
echo $PYTHONPATH
```

**NOTE** that this environment variable will be set and hold true **ONLY** in that terminal session this command was run on.

#### External Function Example
Below is a simple example of calling an external function in a python script under "save:" section of response in a tavern yaml
test file.
```buildoutcfg
# test.tavern.yaml
save:
  $ext:
    function: utils:test_function

# utils.py
from box import Box

def test_function(response):
    return Box({"test_user_name": response.json()["user"]["name"]})
```
In this case, {test_user_name} is available for use in later requests.

#### Documentation
For more information regarding usages of external functions in tavern, refer the below link on official tavern documentation.
 - [External Functions - Tavern Documentation](https://tavern.readthedocs.io/en/latest/basics.html#calling-external-functions)


### Running Cypress tests

We run integration and end-to-end tests specifically against the UI using Cypress.

To run them, please view the README under the [frontend](./frontend/README.md) directory.
