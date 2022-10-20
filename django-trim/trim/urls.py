"""
Short URL to help lighten the load for dev urls

    default:

        from django.urls import path

        urlpatterns = [
            path('', views.ProductListView.as_view(), name='list'),
            path('new/', views.ProductCreateView.as_view(), name='create'),
            path('change/<str:pk>/', views.ProductUpdateView.as_view(), name='update'),
            path('delete/<str:pk>/', views.ProductDeleteView.as_view(), name='delete'),
            path('<str:pk>/', views.ProductDetailView.as_view(), name='detail'),
        ]


    to this:

        from . import models
        from trim.models import grab_models

        urlpatterns = trims.paths_default(views, grab_models(models),
            views=('list', 'create', 'update', 'delete', 'detail',),
        )


    or this:

        from . import models
        from trim.models import grab_models

        urlpatterns = trims.paths_less(views, grab_models(models),
            ignore_missing_views=True,
            list='',
            create='new/',
            update='change/<str:pk>/',
            delete='delete/<str:pk>/',
            detail='<str:pk>/',
        )


"""
from django.contrib import admin
from django.urls import path, include as django_include, reverse
from  django.views.generic import View, TemplateView

import inspect
import sys

from trim.names import *
from . import names as trim_names


from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView



def absolute_reverse(request, name, *args):
    fa_url = reverse(name, args=args)
    return absolutify(request, fa_url)


def absolutify(request, path):
    base_url =  "{0}://{1}{2}".format(
            request.scheme,
            request.get_host(),
            path,
            )
    return base_url


def favicon_path(ingress_path='favicon.ico', static_path='images/{ingress_path}'):
    static_path = static_path.format(ingress_path=ingress_path)
    return static_redirect_path(ingress_path, static_path)


def static_redirect_path(ingress_path, static_path):
    return path(ingress_path,
            RedirectView.as_view(
                url=staticfiles_storage.url(static_path)
                )
            )


urlpatterns = [
    # path('admin/', admin.site.urls),
]


def clean_str(variant):

    if variant in (False, None,):
        return ''
    return variant


def path_includes(*names):

    flat_names = ()
    r = {}

    for name in names:
        if isinstance(name, (list,tuple)) is False:
            name = (name, )
        flat_names += name

    for fln in flat_names:
        # print('Making', fln)
        r[fln] = f'{fln}/', django_include(f'{fln}.urls')

    return paths(**r)

include = path_includes

def path_urls(views, path_rels):
    for url, view_call in path_rels:
        pass


def index(name):
    return


def path_include(url_name, url_module=None, path_name=None):
    """
        path_include('products/',)
        path_include('mythings/', 'products.urls', ) # name=mythings
        path_include('mythings/', 'products.urls', 'items') # name=items
        path_include('products/', 'products.urls', 'products')

    Apply like this:

        from django.contrib import admin
        from django.urls import path, include

        from trim.urls import path_include, path_includes, error_handlers

        app_name = 'shoppinglist'

        urlpatterns = [
            path('admin/', admin.site.urls),
        ] + path_includes('products')

        error_handlers(__name__)
    """
    r = {}
    url = url_name
    if not url.endswith('/'):
        url = f'{url}/'

    name = path_name or url_name
    if name.endswith('/'):
        name = name[1:]

    urlm = url_module or f'{name}.urls'
    r[name] = (url, django_include(urlm), )

    return paths(**r)


def paths_default(views_module, model_list, ignore_missing_views=True, views=None, **options):
    """
        from . import models
        from trim.models import grab_models

        urlpatterns = trims.paths_default(views, grab_models(models),
            ignore_missing_views=True,
            views=('list', 'create', 'update', 'delete', 'detail',),
        )
    """
    patterns = {}

    for name in views:
        url = trim_names.get_url(name)
        patterns[name] = url

    return paths_less(
            views=views_module,
            model_list=model_list,
            ignore_missing_views=ignore_missing_views,
            **patterns)


def paths_less(views, model_list, ignore_missing_views=False, **patterns):
    """
        from . import models
        from trim.models import grab_models

        urlpatterns = trims.paths_less(views, grab_models(models),
            ignore_missing_views=True,
            list='',
            create='new/',
            update='change/<str:pk>/',
            delete='delete/<str:pk>/',
            detail='<str:pk>/',
        )

    """
    if isinstance(model_list, (list, tuple,)) is False:
        model_list = (model_list,)

    r = []
    for m in model_list:
        name = m.__name__
        unp = name.lower()
        url_pattern_prefix=f'{unp}/'
        r += paths_named(views, name,
            url_pattern_prefix=url_pattern_prefix,
            ignore_missing_views=ignore_missing_views,
            url_name_prefix=f'{unp}-',
            **patterns)
    return r


def paths_named(views, view_prefix=None, ignore_missing_views=False, url_pattern_prefix=None,
        url_name_prefix=None, **patterns):
    """
        urlpatterns = trims.paths_named(views,
            view_prefix='Product',

            list=('ListView',''),
            create=('CreateView','new/'),
            update=('UpdateView','change/<str:pk>/'),
            delete=('DeleteView','delete/<str:pk>/'),
            detail=('DetailView','<str:pk>/'),
        )

    or less:

        from trim import urls as trims

        urlpatterns = trims.paths_named(views,
            view_prefix='Product',
            # name_genfix="{view_prefix}{mapped_name}View",
            list='',
            create='new/',
            update='change/<str:pk>/',
            delete='delete/<str:pk>/',
            detail='<str:pk>/',
        )
    """
    new_patterns = {}
    for app_name, solution in patterns.items():
        if isinstance(solution, (list, tuple,)) is False:
            # only a URL given.
            # convert the 'list' to 'ListView'
            solution = (MAPPED_NAMES.get(app_name), solution)

        class_name, url, *extra = solution
        new_patterns[class_name] = (app_name, url,) + tuple(extra)

    return paths_dict(views, new_patterns, view_prefix,
        url_pattern_prefix=url_pattern_prefix,
        url_name_prefix=url_name_prefix,
        ignore_missing_views=ignore_missing_views)


def paths_tuple(views, patterns, **kw):
    """Setup URLS using a tuple of tuples, with each given tuple prepared
    and passed to the paths_dict:

        from trim import urls as trims

        trim_patterns = (
            ('NoteIndexView', 'index', '' ),
            ('EntryJsonList', 'entity-list-json', 'entry/list/json/' ),
            ('EntryDetailView', 'entry-detail-json', '<str:pk>/json/' ),
        )

        urlpatterns = trims.paths_tuple(views, trim_patterns)

    Of which is the same as:

        from trim import urls as trims

        trim_patterns = dict(
            NoteIndexView=('index', ''),
            EntryJsonList=('entity-list-json', 'entry/list/json/',),
            EntryDetailView=('entry-detail-json', '<str:pk>/json/', ),
        )

        urlpatterns = trims.paths_dict(views, trim_patterns)
    """
    d_patt = {}

    for key, *params in patterns:
        d_patt[key] = params

    return paths_dict(views, d_patt, **kw)


def paths_dict(views, patterns=None, view_prefix=None,
    ignore_missing_views=False,
    url_pattern_prefix=None,
    url_name_prefix=None,
    safe_prefix=False,
    **kw,
    ):
    """Given the views module and the patterns,
    generate a shjort path list.

        trim_patterns = {
            'ProductListView': '',
            'ProductCreateView': ('create', 'new/'),
            'ProductUpdateView': ('update', 'change/<str:pk>/'),
            'ProductDeleteView': 'delete/<str:pk>/',
            'ProductDetailView': '<str:pk>/',
        }

        urlpatterns = trims.paths_dict(views, trim_patterns)

        trim_patterns = dict(
            ListView='',
            CreateView=('create', 'new/'),
            UpdateView=('update', 'change/<str:pk>/'),
            DeleteView='delete/<str:pk>/',
            DetailView='<str:pk>/',
        )

        urlpatterns = trims.paths_dict(views, trim_patterns, view_prefix='Product')
        urlpatterns = trims.paths_dict(views, trim_patterns, view_prefix='People')

    """
    flag_class = View
    # r = ()
    d = {}
    patterns = patterns or {}
    view_prefix = clean_str(view_prefix)
    url_pattern_prefix = clean_str(url_pattern_prefix)
    url_name_prefix = clean_str(url_name_prefix)

    patterns.update(kw)

    for part_name, solution in patterns.items():
        class_name = f"{view_prefix}{part_name}"

        try:
            view = getattr(views, class_name)
        except AttributeError as e:

            if ignore_missing_views is False:
                raise e
            continue

        if isinstance(solution, (list, tuple,)) is False:
            current_name = class_name.lower()
            last_name = inspect.getmro(view)[1].__name__
            app_name = MAPPED_CLASS.get(last_name, current_name)
            solution = (app_name, solution,)

        path_name, url, *extra = solution

        furl = f'{url_pattern_prefix}{url}'
        fname = f'{url_name_prefix}{path_name}'
        if (fname in d) or (safe_prefix is True):
            fname = f"{part_name.lower()}-{fname}"
        d[fname] = (furl, view,) + tuple(extra)



    r = paths(**d)

    return r



def template_view(url_string, html_path, name='template_view'):

    # urlpatterns += [
    #     trims.template_view('mockup/', 'mockup/crystal-geometries.html')
    # ]

    return path(url_string, TemplateView.as_view(template_name=html_path), name=name)


def as_templates(**props):
    """

        urlpatterns += trims.as_templates(
            geoms=('mockup/', 'mockup/crystal-geometries.html')
        )

    """
    return [template_view(*v, name=k) for k,v in props.items()]


from functools import reduce


def paths(**path_dict):
    """
        urlpatterns = trims.paths(
            list=('', views.ProductListView,),
            create=('new/', views.ProductCreateView,),
            update=('change/<str:pk>/', views.ProductUpdateView,),
            delete=('delete/<str:pk>/', views.ProductDeleteView,),
            detail=('<str:pk>/', views.ProductDetailView,),
        )

        urlpatterns = [
            path('', views.ProductListView.as_view(), name='list'),
            path('new/', views.ProductCreateView.as_view(), name='create'),
            path('change/<str:pk>/', views.ProductUpdateView.as_view(), name='update'),
            path('delete/<str:pk>/', views.ProductDeleteView.as_view(), name='delete'),
            path('<str:pk>/', views.ProductDetailView.as_view(), name='detail'),
        ]

    """
    flag_class = View
    r = ()
    for name, params in dict(path_dict).items():
        (url, unit, *extra) = params
        func = unit
        if isinstance(func, tuple) is False:
            if inspect.isfunction(func) is False:

                mros = inspect.getmro(unit)
                if flag_class in mros:
                    view_params = {k: v for d in extra for k, v in d.items()}
                    func = unit.as_view(**view_params)
        print('Makeing', url, func,name)
        p = path(url, func, name=name)
        r += (p,)

    return list(r)


def error_handlers(name, setup=None, template_dir=None):
    """Implement the urls for the given module name

        error_handers(__name__)
        error_handers(__name__, {
                400: 'trims.views.errors.handler400',
                403: 'trims.views.errors.handler403',
                404: 'trims.views.errors.handler404',
                500: 'trims.views.errors.handler500',
            }, template_dir='trim/errors/'
        )

    """

    defaults = {
        400: 'trim.views.errors.handler400',
        403: 'trim.views.errors.handler403',
        404: 'trim.views.errors.handler404',
        500: 'trim.views.errors.handler500',
    }
    default_template_dir = 'trim/errors/'
    template_dir = template_dir or default_template_dir
    defaults.update(setup or {})

    # rebuild the handler function names and set into the target module.
    _package, _module = name.split('.')
    # class_module_name = f'{_package}.views'
    module = sys.modules[name]

    # Push the new handler name into the targt module (shoppinglist.urls)
    for error_num, handler_path in defaults.items():
        handler_name = f'handler{error_num}'
        setattr(module, handler_name, handler_path)
