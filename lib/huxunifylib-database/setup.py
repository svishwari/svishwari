"""
database setup code for the huxunify package
"""
from setuptools import setup, find_namespace_packages

setup(
    name="huxunifylib",
    use_scm_version={
        "root": "../..",
        "relative_to": __file__,
        "local_scheme": "node-and-timestamp",
        "fallback_version": "0.1.0",
    },
    packages=find_namespace_packages(include=["huxunifylib.*"]),
)
