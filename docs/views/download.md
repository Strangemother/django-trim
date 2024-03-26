# Download

Provide large downloads through your view using `streamfile_response`.

```py
from trim.views import streamfile_response, TemplateView


class DownloadAssetView(TemplateView):
    template_name = "example/download_view.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        real_path = context['path']
        name = context['filename']
        return streamfile_response(real_path, name)
        # return self.render_to_response(context)
```