from pathlib import Path

from django.http import FileResponse


def content_type_response(filepath, ext=None, content_types=None, default=None):
    """Return a `FileResponse` type with the Content-Disposition applied.

    from trim.response import content_type_response

    real_filepath = Path('real/file.js')
    return content_type_response(real_filepath)

    """
    default = default or "application/octet-stream"

    content_type_map = content_types or {
        "png": "image/png",
        "pdf": "application/pdf",
        "unknown": default,
    }

    content_type = content_type_map.get(Path(filepath).suffix[1:], default)

    response = FileResponse(filepath.open("rb"), content_type=content_type)

    response["Content-Disposition"] = "filename={}".format(filepath.name)
    return response


def content_data_response(filedata, filename, content_types=None, default=None):
    """Return a `FileResponse` type with the Content-Disposition applied.

    from trim.response import content_type_response

    real_filedata = Path('real/file.js')
    return content_type_response(real_filedata)

    """
    default = default or "application/octet-stream"

    content_type_map = content_types or {
        "png": "image/png",
        "pdf": "application/pdf",
        "unknown": default,
    }

    content_type = content_type_map.get(Path(filename).suffix[1:], default)

    response = FileResponse(filedata, content_type=content_type)
    response["Content-Disposition"] = "filename={}".format(filename)
    return response
