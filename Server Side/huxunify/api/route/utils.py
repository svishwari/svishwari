"""
purpose of this file is to house route utilities
"""


def add_view_to_blueprint(self, rule, endpoint, **options):
    """This decorator takes a blueprint and assigns the view function directly
    the alternative to this is having to manually define this in app.py
    or at the bottom of the route file, as the input is a class.

    app.add_url_rule(
        '/colors/<palette>',
        view_func=PaletteView.as_view('colors'),
        methods=['GET']
    )

    Example: @rabbit_hole(cdm_bp, "/datafeeds", "DatafeedSearch")
    ---

    Args:
        self (func): a flask/blueprint object, must have 'add_url_rule'
        rule (str): an input rule
        endpoint (str): the name of the endpoint

    Returns:
        Response: Returns a datafeed by ID.

    """

    def decorator(cls):
        """decorator function
        ---

        Args:
            cls (object): a function to decorate
        Returns:
            Response: Returns the decorated object.

        """
        # add the url to the flask object
        self.add_url_rule(rule, view_func=cls.as_view(endpoint), **options)
        return cls

    return decorator
