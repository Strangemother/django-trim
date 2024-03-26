import os
import mimetypes


from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str


def streamfile_response(real_filepath, output_filename, chunk_size=8192, content_type=None):
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
    wrapper = FileWrapper(open(real_filepath, "rb"), chunk_size)
    content_type = content_type or mimetypes.guess_type(real_filepath)[0]
    response = StreamingHttpResponse(wrapper,
                    content_type=content_type,
                    # mimetype='application/force-download',
                )
    # response = HttpResponse(mimetype='application/force-download')
    response["Content-Length"] = os.path.getsize(real_filepath)
    sfn = smart_str(output_filename)
    response['Content-Disposition'] = f'attachment; filename={sfn}'
    response['X-Sendfile'] = smart_str(real_filepath)
    # You can also set any other required headers: Cache-Control, etc.
    return response

