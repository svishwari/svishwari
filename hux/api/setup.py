"""Setup code for the huxunify package."""
from setuptools import setup

setup(
    use_scm_version={
        "root": "../..",
        "relative_to": __file__,
        "local_scheme": "node-and-timestamp",
        "fallback_version": "0.1.0",
    },
    include_package_data=True,
)
