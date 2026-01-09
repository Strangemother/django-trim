from pathlib import Path
import os


def recombine(dir_path, output_filepath=None):
    """Given a Directory of many parts, merge the files into
    one.
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
