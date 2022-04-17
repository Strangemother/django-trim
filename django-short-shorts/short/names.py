
VIEWS = (

    ## crud
    'ListView',
    'CreateView',
    'UpdateView',
    'DeleteView',
    'DetailView',
    # 'DeleteViewCustomDeleteWarning',

    ## history
    'ArchiveIndexView',
    'DateDetailView',
    'DayArchiveView',
    'MonthArchiveView',
    'TodayArchiveView',
    'WeekArchiveView',
    'YearArchiveView',

    'RedirectView',
    'TemplateView',

    'FormView',
    'LoginView',
    'LogoutView',

    'PasswordChangeDoneView',
    'PasswordChangeView',
    'PasswordResetCompleteView',
    'PasswordResetConfirmView',
    'PasswordResetDoneView',
    'PasswordResetView',

)

## Order is importtant.
url_enforcements = (
    ( ('update', 'detail', 'delete',), '{name}/<str:pk>/', ),
    # ( ('archiveindex',), '', ),
    ( ('todayarchive',), 'today/', ),
    ( ('datedetail',  ), '<int:year>/<str:month>/<int:day>/<int:pk>/', ),
    ( ('dayarchive',  ), '<int:year>/<str:month>/<int:day>/', ),
    ( ('montharchive',), '<int:year>/<str:month>/' , ),
    ( ('weekarchive', ), '<int:year>/week/<int:week>/', ),
    ( ('yeararchive', ), '<int:year>/', ),
)

## Generate a Mapped name lise of the VIEWS, producing a list for direct
## name association:
    # 'list':'ListView',
    # 'create':'CreateView',
    # 'update':'UpdateView',
    # 'delete':'DeleteView',
    # 'detail':'DetailView',
MAPPED_NAMES = { x[:-4].lower(): x for x in VIEWS }

## Write the reverse of the MAPPED_NAMES, for class to friendly map:
    # ListView: list
MAPPED_CLASS = {y:x for x,y in MAPPED_NAMES.items()}


def crud():
    return (
        'list',
        'create',
        'update',
        'delete',
        'detail',
        )

def history():
    # Order is important
    return (
        'archiveindex',
        'todayarchive',
        'weekarchive',
        'datedetail',
        'dayarchive',
        'montharchive',
        'yeararchive',
    )

def tidy_enforcements(enforcements):
    url_parts = {}
    for names, enforced in enforcements:
        for n in names:
            url_parts[n] = enforced
    return url_parts


def render_defaults(names, parts):
    refs = {}
    res = {}
    for name, classname in names.items():
        refs['name'] = name
        refs['classname'] = classname
        live_part = parts.get(name, None)
        first = f'{name}/'
        part = ''
        if live_part is not None:
            part = live_part.format(**refs)
            first = ''
        res[name] = f'{first}{part}'
    return res


URL_PARTS = tidy_enforcements(url_enforcements)
URL_DEFAULTS = render_defaults(MAPPED_NAMES, URL_PARTS)

def get_url(name):
    return URL_DEFAULTS.get(name)

import inspect

def get_mapped_name(instance):
    mro = inspect.getmro(instance.__class__)
    for _c in mro:
        r = MAPPED_CLASS.get(_c.__name__)
        if r is not None:
            return r
