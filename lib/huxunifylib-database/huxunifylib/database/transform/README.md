# Transformer utilities

A set of constants with corresponding methods for dataframe field transformations including PII normalizing and hashing.

## Usage

To configure the transformation process for each PII field of interest use the
following constants:
* **TransformerNames**: Transformer names. Each name corresponds to transformation method.
* **TransformerConfig**: Configuration for each transformer:
  * **SOURCE_COLUMN_NAMES**: source column names.
  * **DESTINATION_COLUMN_NAME**: destination column name.
  * **REMOVE_SOURCE_COLUMNS**: indication if source columns are to be removed after all transformations have been completed.


For each platform audiences are delivered to (e.g. Walled Garden) define configuration for each PII field in the following format:

```python
from huxunifylib.database.transform.const import TransformerNames
from huxunifylib.database.datarouter.const import TransformerConfig

wg_pii_config = {
    TransformerNames.EMAIL.name: {
        TransformerConfig.SOURCE_COLUMN_NAMES.name: ["RawEmail"],
        TransformerConfig.DESTINATION_COLUMN_NAME.name: "HashedEmail",
        TransformerConfig.REMOVE_SOURCE_COLUMNS.name, True
    },

    TransformerNames.PHONE_E164.name: {
        TransformerConfig.SOURCE_COLUMN_NAME.name: ["RawPhone"],
        TransformerConfig.DESTINATION_COLUMN_NAME.name: "HashedPhone",
    },

    # ... Other PII transformer methods used ...
}
```
from huxunifylib.util.transform.const import TransformerNames

To perform transformation on **dataframe** use **TransformerNames**, predefined transformers that are registered in registry **transformer_registry**.

```python
from huxunifylib.util.datarouter.const import TransformerConfig
from huxunifylib.util.transform.methods import (
    transformer_registry as method_registry
)


    for transformer_name, transformer_config in transform_config.items():

        src_columns_to_remove, dst_columns = set(), set()

        src_col_names = transformer_config[
            TransformerConfig.SOURCE_COLUMN_NAMES.name
        ]
        dst_col_name = transformer_config[
            TransformerConfig.DESTINATION_COLUMN_NAME.name
        ]

        # By default always remove source column to avoid retaining
        # PII data accidentally
        if transformer_config.get(
            TransformerConfig.REMOVE_SOURCE_COLUMNS.name, True
        ):
            src_columns_to_remove = src_columns_to_remove.union(
                set(src_col_names)
            )
            dst_columns.add(dst_col_name)

        transformer_method = method_registry.get(transformer_name, None)
        if not transformer_method:
            raise HuxAdvException  # TODO raise Wrong Transformer Name exception

        # Apply method
        dataframe[dst_col_name] = dataframe.apply(
            lambda x: transformer_method(*[x[col] for col in src_col_names]),
            axis=1,
        )

    # Drop all source columns slated for removal except
    # detination columns
    src_columns_to_remove = src_columns_to_remove.difference(dst_columns)
    dataframe = dataframe.drop(src_columns_to_remove, axis=1)

    return dataframe
```
