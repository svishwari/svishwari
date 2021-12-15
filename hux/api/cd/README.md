## Adding environment/pipeline/promote variables in config.env files

- Each `config.env` file contains environment/trigger specific variables to be used in codefresh promote pipeline, which is maintained in respective trigger-specific folders.

- Directory structure should follow this standard : 

```sh
 ├── trigger-1/
 │   ├── config.env
 ├── trigger-2/
 │   └── config.env                           
 ├── ...
```

Here `trigger-1, trigger-2` refers to the trigger name which is set in the codefresh UI.

- For each trigger in codefresh-pipeline, a `config.env` file needs to be maintained.

- **Note**: While creating `config.env` files, make sure to add an empty line in the end of the file. If not added, codefresh will add an extra character in the end of the file which will lead to wrong variable value.

