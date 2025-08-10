# Considerations

As I progress through the tools I need, I note the extra elements here and see if they're useful later.


## Auto save

The save feature compiles the pre-md to md into the output dir. The autosave should cache the user editor input into a store point. Upon user acted "save", the file is written and the cache is scrubbed.

The save content can exist in the DB, as a _cache_ record for the file. Alternatively an `*.autosave` file can replace a db record.

## Naming

The edited record shouldn't be output record as a _save_ would overwrite the tags. functionality.
