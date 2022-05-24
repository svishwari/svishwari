===========
HUX Unified
===========

Documentation for HUS User Experience Platform.

Rendered Documentation
----------------------
Following are the different versions of documentation and the corresponding branch/tag they are rendered from.

* `Latest <https://docs.hux.deloitte.com/docs/hux-unified/en/latest/>`_ - Built from main branch of the repo.
* `Stable <https://docs.hux.deloitte.com/docs/hux-unified/en/stable/>`_ - Built from the most recently released tag in main branch of the repo.
* `Develop <https://docs.hux.deloitte.com/docs/hux-unified/en/develop/>`_ - Built from develop branch of the repo.

RTD Docs local build
--------------------
Follow the below instructions to build and render the RTD docs locally.

1. Change to docs directory as current working directory.
    a. cd hux-unified/docs
2. Install the below packages using pip command.
    a. pip install sphinx
    b. pip install sphinxcontrib-spelling
3. Build the sphinx style RTD docs using the following command.
    a. make html
4. Start a simple http server using python3.
    a. python -m http.server
5. Go to the below URL to view the built RTD html files.
    a. http://localhost:8000/build/html/index.html

In addition to the building and viewing the RTD sphinx docs locally, all the docs validation that are run
as part of CI pipeline can be run within a tox environment using the tox.ini file in the docs directory.

1. Change to docs directory as current working directory.
    a. cd hux-unified/docs
2. Run the tox command to run the validations included in tox.ini file.
    a. tox
