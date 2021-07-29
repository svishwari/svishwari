Purpose of this folder is to house all the integration tests for the API and UI.

### Running tests
```
# cd to this folder
pip install pip -U
pip install tavern

# run pytest
py.test -v
```

### Sample Output
```
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

PYTHONPATH environment variable can be set on a terminal session depending on the environment as shown below.

#### Windows
```buildoutcfg
SET PYTHONPATH=%PYTHONPATH%;<absolute_path_to_script>
```

#### Mac/Linux
```buildoutcfg
PYTHONPATH=$PYTHONPATH:<absolute_path_to_script>
```

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
