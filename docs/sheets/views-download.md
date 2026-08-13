# Views: File Responses

`trim.views.download` provides streaming responses for downloads and range-aware media delivery.

## Import

```py
from trim.views.download import stream, streamfile_response
```

## stream

`stream(request, path)` returns a `StreamingHttpResponse` and supports HTTP byte ranges:

```py
from trim.views.download import stream

class VideoView(views.View):
    def get(self, request, *args, **kwargs):
        return stream(request, "/srv/media/video.mp4")
```

Behavior:

- Detects the content type from the path and falls back to `application/octet-stream`.
- Handles `Range` requests with status `206` and a `Content-Range` header.
- Adds `Accept-Ranges: bytes`.
- Streams the full file with status `200` when no range is supplied.

## streamfile_response

Use `streamfile_response` when the response should be an attachment with a download filename:

```py
from trim.views.download import streamfile_response

class ExportView(views.View):
    def get(self, request, *args, **kwargs):
        return streamfile_response(
            "/srv/exports/report.csv",
            "report.csv",
        )
```

Signature:

```py
streamfile_response(
    real_filepath,
    output_filename,
    chunk_size=8192,
    content_type=None,
    range_header=None,
)
```

It sets `Content-Disposition`, `Content-Length`, `Accept-Ranges`, `X-Sendfile`, and the detected or supplied content type. A valid `range_header` produces a partial response.

## RangeFileWrapper

`RangeFileWrapper` is the lower-level iterator used for partial file reads:

```py
from trim.views.download import RangeFileWrapper

with open("/srv/media/video.mp4", "rb") as handle:
    chunks = RangeFileWrapper(handle, offset=1024, length=4096)
    for chunk in chunks:
        process(chunk)
```

Constructor options are `stream`, `chunk_size=8192`, `offset=0`, and `length=None`. Call `close()` when using it outside a response lifecycle.

## Security Note

Neither helper authorizes access or validates paths. Resolve paths from trusted identifiers, enforce permissions, and prevent directory traversal before calling them. Never pass an unvalidated user-supplied filesystem path directly to these functions.
