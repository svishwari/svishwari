# Hux Unified API

[![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/deloittehux/Hux_Unified_Solution%2Funified_solution_api_ci?type=cf-1&key=eyJhbGciOiJIUzI1NiJ9.NWRjMzBjMmJiMGVmMzJiNzkxM2Y2MGJh.GkhczDGoVzfrLnhTAn2b9yqwMQkP_wXNMhwGDPRPStQ)]( https://g.codefresh.io/pipelines/edit/new/builds?id=605a45789f86ae45939bfec3&pipeline=unified_solution_api_ci&projects=Hux_Unified_Solution&projectId=605a4546bfffd0aea1e243a0)

Hux Unified API is an API that will be primarily consumed by the
Hux Unified Front-end application.

The API is UI-driven.

## Installation
```
# clone the repo
git clone https://github.com/DeloitteHux/hux-unified.git

# cd to the hux/api repo
cd hux-unified/hux/api

# install pipenv
pip install pipenv

# run pipenv install
pipenv install

# activate the virtual environment
pipenv shell
```

## Environment Variables
The API consumes environment variables from the settings.ini file.
For more information, see the link below.
https://github.com/henriquebastos/python-decouple

Decouple always searches for Options in this order:
1. Environment variables
2. Repository: ini or .env file
3. Default argument passed to config.

#### Setup
```
# cd to the hux/api folder
cd hux-unified/hux/api

# download the public ssl cert for aws
wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

# copy the template-settings.ini file
cp template-settings.ini settings.ini

# now populate all the env variables in that file.
```

### Connecting to the UNIFIED Environment.
A user must be connected to the AWS VPN for accessing the database and unified domains.
Instructions for connection can be followed here
 - [AWS Client VPN](https://confluence.marketingservices.deloitte.com/pages/viewpage.action?spaceKey=TO&title=How-To%3A+Authenticate+to+AWS+console%2C+API%2C+terragrunt%2C+VPN+using+Okta+for+End+Users#HowTo:AuthenticatetoAWSconsole,API,terragrunt,VPNusingOktaforEndUsers-AWSClientVPNapp)

### Generating AWS Credentials
For connecting to AWS, a user must generate AWS credentials via OKTA.
Instructions can be found here
 - [Accessing AWS Console](https://confluence.marketingservices.deloitte.com/pages/viewpage.action?spaceKey=TO&title=How-To%3A+Authenticate+to+AWS+console%2C+API%2C+terragrunt%2C+VPN+using+Okta+for+End+Users#HowTo:AuthenticatetoAWSconsole,API,terragrunt,VPNusingOktaforEndUsers-AWSConsoleAccessapp)

### Software Dependencies

Python Version
* Python 3.7


#### Flasgger
Flasgger is a Flask extension to **extract [OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#operation-object)**
from all Flask views registered in your API.

Flasgger also comes with **[SwaggerUI](http://swagger.io/swagger-ui/) embedded** so you can access [http://localhost:5000/apidocs](localhost:5000/apidocs)
and visualize and interact with your API resources.

#### flask-marshmallow

Flask-Marshmallow is a thin integration layer for **[Flask](http://flask.pocoo.org/)** (a Python web framework)
and **[marshmallow](http://marshmallow.readthedocs.io/)** (an object serialization/deserialization library)
that adds additional features to marshmallow, including URL and Hyperlinks fields for HATEOAS-ready APIs.
It also (optionally) integrates with **[Flask-SQLAlchemy](http://marshmallow.readthedocs.io/)**.

#### apispec

apispec is a pluggable API specification generator. Currently, supports the **extract [OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#operation-object)**

### Docker
For building the docker locally, follow the steps below
```
# starting from the parent folder of the repo
# assumes docker is installed

# pull python3.7-slim-buster
docker pull python@sha256:5375725c3c0a0215279c1c5ddb33f91d31f0eb37010140397e5c7e5530073d2c

# change the repo line in hux/api/Dockerfile to the following.
FROM python:3.7-slim-buster AS hux-unified

# build the docker
sudo docker build . -f ./hux/api/Dockerfile --build-arg ARTIFACTORY_PYTHON_READ=https://{user_name@deloitte.com}:{jfrog_key}@repo.mgnt.in/artifactory/api/pypi/python/simple --tag hux-unifed-test

# after it is built, run it to test
sudo docker run -p 5000 hux-unifed-test
```

## Usage

Here's an example of basic usage
```
# cd to the hux/api folder
cd hux-unified/hux/api

# add the current directory to python path
PYTHONPATH=$PYTHONPATH:`pwd`

# run the flask app
python huxunify/app.py
```

API Usage
 - SWAGGER DOCS: http://0.0.0.0:5000/api/v1/ui
 - HEALTH CHECK: http://0.0.0.0:5000/health-check


![apidocs.png](apidocs.png)

## Style Guide

### pylint
We use a series of pylint checks for this project.
They can be found [here](https://github.com/DeloitteHux/hux-unified/blob/main/.pylintrc)

pylint can be configured within your IDE.
Here is how to configure for the common IDEs:

#### Visual Studio Code
https://code.visualstudio.com/docs/python/linting

#### PyCharm
https://www.jetbrains.com/help/pycharm/configuring-third-party-tools.html
https://plugins.jetbrains.com/plugin/11084-pylint

### Black
python Black enforces formatting, for more information see the black [homepage](https://black.readthedocs.io/en/stable/installation_and_usage.html#:~:text=Black%20can%20be%20installed%20by%20running%20pip%20install,hotness%20and%20want%20to%20install%20from%20GitHub%2C%20use%3A)
We configure Black within our project by using pyproject.toml files.

With IDE integration, a user can configure black so that it automatically runs on file save.

here is how to configure for the common IDEs

#### PyCharm
https://black.readthedocs.io/en/stable/editor_integration.html#pycharm-intellij-idea

#### Visual Studio Code
https://black.readthedocs.io/en/stable/editor_integration.html#visual-studio-code

### Docstrings
Google Python Docstrings
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

```
def generate_synthetic_marshmallow_data(schema_obj: Schema) -> dict:
    """This function generates synthetic data for marshmallow

    Args:
        schema_obj (Schema): a marshmallow schema object

    Returns:
        dict: a dictionary that simulates the passed in marshmallow schema obj

    """
    # get random data based on marshmallow type
    return {
        field: SPEC_TYPE_LOOKUP[type(val)] for field, val in schema_obj().fields.items()
    }
```

### Typehinting and Docstrings
```
def generate_synthetic_marshmallow_data(schema_obj: Schema) -> dict:
    """This function generates synthetic data for marshmallow

    Args:
        schema_obj (Schema): a marshmallow schema object

    Returns:
        dict: a dictionary that simulates the passed in marshmallow schema obj

    """
    # get random data based on marshmallow type
    return {
        field: SPEC_TYPE_LOOKUP[type(val)] for field, val in schema_obj().fields.items()
    }
```

### Testing
```
# cd to the hux/api folder
cd hux-unified/hux/api

# add current directory to python path
PYTHONPATH=$PYTHONPATH:`pwd`

# run the unittest
python -m unittest
```

## Database
Huxunify connects to a DocumentDB via [pymongo](https://pymongo.readthedocs.io/en/stable/index.html)

### Connection to the database
There are two primary ways for connecting to the database

1. Using the command line - instructions [here](https://docs.mongodb.com/manual/mongo/#:~:text=You%20can%20use%20the%20command-line%20option%20--host%20%3Chost%3E%3A%3Cport%3E.,the%20--host%20%3Chost%3E%20and%20--port%20%3Cport%3E%20command-line%20options.)
2. Using a GUI such as MongoDB Compass [here](https://www.mongodb.com/products/compass)


### How to implement a new endpoint
* Define marshmallow Schema: create a schema by defining a class with variables
mapping attribute names to Field objects. For example:
```
class Fieldmapping(Schema):
    """Fieldmapping schema."""

    field_id = Int(required=True)
    field_name = Str(required=True, validate=validate.OneOf(FIELD_NAMES))
    field_variation = Str(required=True)
    modified = DateTime(required=True)
```

* Add swagger view to route
1. Setup the blueprint, for example:
```
cdm_bp = Blueprint("cdm", import_name=__name__)
```

2. Add view to blueprint, for example:
```
@add_view_to_blueprint(
    cdm_bp, f"/{FIELDMAPPINGS_ENDPOINT}/<field_id>", "FieldmappingView"
)
```

3. Add parameters and responses of the endpoint, for example:
```
    parameters = [
        {
            "name": "field_id",
            "description": "ID of the fieldmapping",
            "type": "integer",
            "in": "path",
            "required": "true",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": Fieldmapping,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
```

4. Add marshal_with(Schema) to the method, for example:
```
@marshal_with(Fieldmapping)
```

5. Add Endpoint Summary and Description

Flasgger uses view functions docstrings to fill the summary and description
The part of the docstring following the '---' line is ignored.

The part before the '---' line is used as summary and description.
The first lines are used as summary.
If an empty line is met, all following lines are used as description.

```
def get(...):
    """Retrieves the processed data source catalog.

    Return processed data sources
    ---
    Returns:
        Response: List of processed data sources.
    """
```

The example above produces the following documentation attributes:
```
{
    'get': {
        'summary': 'Retrieves the processed data source catalog.',
        'description': 'Return processed data sources',
    }
}
```

6. Here is an example of a completed endpoint.
```
@add_view_to_blueprint(cdm_bp, f"/{PROCESSED_DATA_ENDPOINT}", "ProcessedDataSearch")
class ProcessedDataSearch(SwaggerView):
    """
    ProcessedData search class
    """

    parameters = []
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of processed data sources.",
            "schema": ProcessedData,
        }
    }
    tags = [PROCESSED_DATA_TAG]

    @marshal_with(ProcessedData(many=True))
    def get(self):  # pylint: disable=no-self-use
        """Retrieves the processed data source catalog.

        Return processed data sources
        ---
        Returns:
            Response: List of processed data sources.
        """
        return CdmModel().read_processed_sources(), HTTPStatus.OK.value
```
