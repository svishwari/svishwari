Purpose of this folder is to house all the integration tests for the API and UI.

Running tests
```
# cd to this folder
pip install pip -U
pip install tavern

# run pytest
py.test -v
```

Sample Output
```
============================================================================ test session starts ============================================================================
platform darwin -- Python 3.7.9, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /Users/douglaslong/Documents/repos/hux-unified/hux/integration_tests
plugins: tavern-1.16.0, hypothesis-6.14.2, requests-mock-1.9.3, Faker-8.10.1, typeguard-2.12.0
collected 1 item

api/test_core.tavern.yaml .                                                                                                                                           [100%]

============================================================================= 1 passed in 0.62s =============================================================================
```
