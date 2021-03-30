# Hux Unified Solution Server-Side

Information the Server Side Flask Project

## Installation
```
# cd to the hux/api folder
cd "/hux-hunified-solution/api"

# run pipenv install
pipenv install

# activate the virtual environment
pipenv shell

# install the dependencies
pipenv install tox-pipenv
pipenv install
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


### Data

### Search

### Web interface

### Evaluation

[comment]: <> (You will need assessments log file, obtained from server.  )

## Report

## License

Private
