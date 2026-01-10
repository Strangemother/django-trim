import os
from pathlib import Path


def recombine(dir_path, output_filepath=None):
    """
    Merge multiple split file parts from a directory into a single file.

    This function takes a directory containing split file parts (typically with
    extensions like .part_0, .part_1, etc.) and recombines them into a single
    output file. The parts are merged in numerical order based on their suffix.

    Args:
        dir_path (str or Path): The directory path containing the split file parts
            to be recombined.
        output_filepath (str or Path, optional): The path where the merged file
            should be written. Can be either a file path or a directory path.
            If a directory is provided, the output filename will be derived from
            the first part file (without the .part_N extension). If None, defaults
            to the input directory. Defaults to None.

    Returns:
        Path: The Path object pointing to the created merged file.

    Raises:
        FileExists: If the output file already exists at the specified location.

    Examples:
        Merge parts in a directory to the same directory:

            >>> output = recombine('/path/to/parts/')
            >>> # Creates merged file in /path/to/parts/filename

        Specify a custom output file path:

            >>> output = recombine('/path/to/parts/', '/output/merged.zip')
            >>> print(output)
            /output/merged.zip

        Specify an output directory:

            >>> output = recombine('/path/to/parts/', '/output/dir/')
            >>> # Creates merged file in /output/dir/filename

    Notes:
        - Part files must have extensions in the format .part_0, .part_1, etc.
        - Parts are sorted numerically before merging
        - The function prints progress information during the merge process
        - The output file size is printed upon completion
        - If output file exists, FileExists exception is raised to prevent overwriting

    See Also:
        split_i: Helper function used to extract part numbers for sorting
    """

    # get all files
    dir_files = os.listdir(dir_path)
    print("Found", len(dir_files))

    newname = Path(dir_files[0]).stem  # drops the .part_0

    # same DIR, file is the first part.
    output_filepath = Path(output_filepath or dir_path)

    if output_filepath.is_dir():
        # Apply the name
        output_filepath = output_filepath / newname

    print("output_filepath", output_filepath)

    if output_filepath.exists():
        print("Output file exists", output_filepath)
        raise FileExists(output_filepath)

    ordered_files = sorted(dir_files, key=split_i)
    # now merge
    with open(output_filepath, "wb+") as write_stream:
        print("Writing", output_filepath)
        for filename in ordered_files:
            subfile = Path(dir_path) / filename
            print("  ", filename)
            with open(subfile, "rb") as read_stream:
                write_stream.write(read_stream.read())
        print("Complete", output_filepath.name)

    print("Size: ", os.path.getsize(output_filepath))

    return output_filepath


def split_i(item):
    return int(Path(item).suffix.split("_")[1])


class FileExists(Exception):
    pass
