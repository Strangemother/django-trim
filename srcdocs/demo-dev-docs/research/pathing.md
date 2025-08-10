# Paths and Relative Positions

Paths are a minor inconvenience, so going forward the _file position_ is applied early in the view set, giving all assets a value for all relations.

All file target should be relative from the given file - this includes assets (CSS/JS/HTML).

For safety the tool should never break out of the output directory (Root) - this is in reference to the root of the source docs.
