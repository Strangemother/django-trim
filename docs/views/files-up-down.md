# Upload and Download

Django Trim offers a few functions to simplify large file uploads and downloads.

## Download

Provide small or large downloads through your view using `streamfile_response` function.

```py
from trim.views import streamfile_response, TemplateView


class DownloadAssetView(TemplateView):
    template_name = "example/download_view.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        real_path = context['path']
        name = context['filename']

        # return self.render_to_response(context)
        # Respond with a file.
        return streamfile_response(real_path, name)
```

## Upload

For the upload feature, we've opted to supply a more comprehensive tool to allow large file uploads **without complex integration routines**, such as CDN caching or _[insert service here]_ file handling tools.

**How does it work?**

During the upload phase a file is segmented into chunks. Each chunk is stored using a generic file form under a predictable name. Once all chunks are complete, we can merge the file on the server.

### TL:DR;

Supply URL's to the following:

```py

from trim.views.upload import (
    UploadChunkView,
    UploadAssetView,
    MergeAssetView,
    UploadAssetSuccessView
)
```

For example with `trim.urls.paths_named`:

```py
from trim import urls

urlpatterns = urls.paths_named(views,
    upload_chunk=('UploadChunkView', (
            'upload/chunk/',
            'upload/chunk/<str:extra>/',
            )
        ),
    upload=('UploadAssetView', 'upload/file/'),
    merge=('MergeAssetView', 'upload/merge/<str:uuid>/'),
    upload_success=('UploadAssetSuccessView', 'upload/success/<str:uuid>/'),
)
```