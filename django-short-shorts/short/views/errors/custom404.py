
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse


class Missing404RedirectUrl(Exception):
    pass

from django.views.generic import TemplateView


class Custom404TemplateView(TemplateView):
    status_code = 404
    template_name = 'short/errors/404.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['status_code'] = self.status_code
        return kwargs


class Custom404(object):
    """A View mixin to capture disptach 404 and respond with a redirect
    or alternative view
    """
    custom_404_redirect_url = None
    custom_404_redirect = None
    # custom_404_template_name

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return self.custom_404(request, *args, **kwargs)

    def custom_404(self, request, *args, **kwargs):
        """Retutn a 404 response either as a redirect, or inline view replacement.
        If the redirect url exists the user is redirected, if missing, the
        function returns Custom404TemplateView as_view
        """
        if (self.custom_404_redirect_url is None) and (self.custom_404_redirect is False):
            raise Missing404RedirectUrl("custom_404_redirect_url not supplied.")
        custom_404_redirect = self.custom_404_redirect
        if custom_404_redirect is None:
           if self.custom_404_redirect_url is not None:
                custom_404_redirect = True

        if custom_404_redirect is True:
            resolved = self.get_custom_404_url(request, *args, **kwargs)
            return self.custom_404_redirect_response(resolved)
        return self.custom_404_view(request, *args, **kwargs)

    def custom_404_view(self, request, *args, **kwargs):
        props = {}
        n = getattr(self, 'custom_404_template_name', None)
        if n is not None:
            props['template_name'] = self.custom_404_template_name

        ct = Custom404TemplateView.as_view(**props)
        v = ct(request, *args, **kwargs)
        return v

    def get_custom_404_url(self, request, *args, **kwargs):
        if self.custom_404_redirect_url is None:
            raise Missing404RedirectUrl("custom_404_redirect_url not supplied.")
        return reverse(self.custom_404_redirect_url, args=args, kwargs=kwargs)

    def custom_404_redirect_response(self, url):
        return redirect(url)
        # redirect(reverse('products:filter', args=args, kwargs=kwargs))
