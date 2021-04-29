# Hux Unified API

Information the API Flask Project

## Installation
```
# cd to the hux/api folder
cd "/hux-unified/api"

# run pipenv install
pipenv install

# activate the virtual environment
pipenv shell

# install the dependencies
pipenv install tox-pipenv
pipenv install
```

### environmental variables
The API consumes environment variables from the .env file.
For more information see here
https://github.com/henriquebastos/python-decouple

#### Setup
```
# cd to the hux/api folder
cd "/hux-unified/api"

# download the public ssl cert for mongo
wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

# copy the template-settings.ini file
cp template-settings.ini settings.ini

# now populate all the env variabels in that file.
```

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

#### Moto
Moto is a library that allows your tests to easily mock out AWS Services.

#### apispec

apispec is a pluggable API specification generator. Currently, supports the **extract [OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#operation-object)**

### Dev


### Makefile


### Prerequisites

## Usage

### HuxUnify

Start the API
```
FLASK_APP=huxunify.app pipenv run python -m flask run
```

For viewing the API Documentation, simply go to the following URL
.../apidocs

![apidocs.png](apidocs.png)

### Style Guide
PEP8

Google Python Docstrings
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

Typehinting Example
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

### Test
```
pipenv run python -m unittest
```

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



### Data

### Search

### Web interface

### Evaluation

[comment]: <> (You will need assessments log file, obtained from server.  )

## Report

## License

Private
