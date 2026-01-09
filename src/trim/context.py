# from django.core.urlresolvers import resolve
from django.urls import resolve


def appname(request):
    return {"appname": resolve(request.path).app_name}
