import os
import mimetypes

from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
import os
import re

from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str

import re

range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


def stream(request, path):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(
                RangeFileWrapper(
                    open(path, 'rb'),
                    offset=first_byte,
                    length=length
                ),
                status=206,
                content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp


def stream(request, path):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(
                RangeFileWrapper(
                    open(path, 'rb'),
                    offset=first_byte,
                    length=length
                ),
                status=206,
                content_type=content_type)
        # resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        # resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp


class RangeFileWrapper(object):
    def __init__(self, stream, chunk_size=8192, offset=0, length=None):
        self.stream = stream
        self.stream.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.chunk_size = chunk_size

    def close(self):
        if hasattr(self.stream, 'close'):
            self.stream.close()

    def __iter__(self):
        return self

    def next(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.stream.read(self.chunk_size)
            if data:
                return data
            raise StopIteration()

        if self.remaining <= 0:
            raise StopIteration()

        data = self.stream.read(min(self.remaining, self.chunk_size))
        if not data:
            raise StopIteration()

        self.remaining -= len(data)
        return data


def streamfile_response(real_filepath, output_filename, chunk_size=8192, content_type=None, range_header=None):
    """Generate a StreamingHttpResponse for the given `real_filepath`. Return
        directly to the client as the response object, e.g: from `get()`.

            response = streamfile_response('/real/path.zip', 'output_name.zip')

        Elements applied:

        + A wsgi FileWrapper
        + Auto content_type
        + StreamingHttpResponse response object
        + Content-Length
        + Content-Disposition
        + X-Sendfile
    """
    filename = os.path.basename(real_filepath)
    size = os.path.getsize(real_filepath)
    handle = open(real_filepath, "rb")
    # if ranges was given, seek the handle up to the point.
    wrapper = FileWrapper(handle, chunk_size)
    content_type = content_type or mimetypes.guess_type(real_filepath)[0]
    safe_filename = smart_str(output_filename)

    # You can also set any other required headers: Cache-Control, etc.
    response_pv = {
        # for bytes ranging partial downloads
        'Accept-Ranges': 'bytes',
        'Content-Disposition': f'attachment; filename={safe_filename}',
        'X-Sendfile': smart_str(real_filepath),
    }

    status_ref = {}
    # range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header or '')
    if range_match:
        status_ref = {
            'status': 206,
        }

        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        response_pv['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)

        size = length
        wrapper = RangeFileWrapper(handle, offset=first_byte, length=length)

    # response = HttpResponse(mimetype='application/force-download')
    response = StreamingHttpResponse(wrapper,
                    **status_ref, content_type=content_type,
                    # mimetype='application/force-download',
                    )

    response["Content-Length"] = str(size)

    for k,v in response_pv.items():
        response[k] = v
    return response

