## Adding environment variables in .var files

- Each `.var` file contains environment specific variables to be used in codefresh-pipeline. Name of the files should follow this standard : 
    `name_of_trigger.var`
     Here name_of_trigger refers to the trigger name which is set in the respective codefresh-pipeline.

- For each trigger in codefresh-pipeline, respective `.var` file needs to be maintained.

- Note: While creating `.var` files, make sure to add an empty line in the end of the file. If not added, codefresh will add an extra character in the end of the file which will lead to wrong varaible value.
    E.g. 
        ```
        JFROG_REGISTRY=unified-docker-dev-local

        ```
