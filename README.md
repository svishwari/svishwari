# hux-unified
Repository for hux unified


## Introduction
todo


## Table of Contents
* [Technologies](#Technologies)
* [Structure](#Structure)
* [Add pre-commit git hooks](#Add pre commit githooks)
* [TOX](#TOX)
* [CI](#CI)
* [CD](#CD)


## Technologies
* API
    * Python 3.7 (Flask)
* Frontend
    * Vue 2
* Database
    * MongoDB


## Structure
* [documents](docs/README.rst)
* [api](hux/api/README.md)
* [frontend](hux/frontend/README.md)
* [library](lib/README.md)
    * [database](lib/database/README.md) (coming soon)


# Add pre-commit git hooks

Steps

1. Install pre-commit:`pip install pre-commit` in a virtualenv.
2. Define `.pre-commit-config.yaml` with the hooks you want to include. If you already have it, you can skip this step.
3. Execute `pre-commit install` to install git hooks in your `.git/hooks` directory.

Note: In case there are changes in the `.pre-commit-config.yaml`, it is a good idea to run `pre-commit clean`.

Every time you try to commit, checks in the pre-commit hook will run and you will not be allowed to commit if there are any errors.
You can also run `pre-commit run` to make sure there are no errors before comitting your code.

For more info, refer https://pre-commit.com/.


# TOX
tox (https://tox.readthedocs.io/) is a tool for running tests in multiple virtualenvs.
TOX configuration files (tox.ini) will run the scripted tests and commands listed within.

Steps

1. Install tox:`pip install tox` in a virtualenv.
2. Using the console, cd to the directory you want to test that contains a tox.ini
3. Run `tox`


# CI
TODO - fill this out


# CD
TODO - fill this out
