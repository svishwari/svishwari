# Sphinx Set up

Steps for setting up Sphinx and autogenerating documentation

## Installation

.. code-block::

    $ Check requirements

## Quickstart

.. code-block::

    $ mkdir docs (if you are setting up docs for the first time)
    $ cd docs
    $ sphinx-quickstart (if you are setting up docs for the first time). Make sure to select seperate source and build dir
    $ sphinx-apidoc -f -o source/ ../hux/api/ ../hux/api/huxunify/test/*


If you have already generated .rst files, you can create html docs using
    $ make html
    $ open build/html/index.html
