import sys
import inspect
from pathlib import Path

from django.apps import apps
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    FormView,
    View,
)

from django.views.generic.dates import (
    ArchiveIndexView,
    DateDetailView,
    DayArchiveView,
    MonthArchiveView,
    TodayArchiveView,
    WeekArchiveView,
    YearArchiveView,
)

from django.contrib.auth import get_user_model


from trim import names as trim_names


ALL = '__ALL__'


class ShortMixin:

    def get_template_names(self):
        v = super().get_template_names()
        mapped_name = trim_names.get_mapped_name(self)
        p = Path(v[0])
        name = p.stem.replace(f'{self.model.__name__.lower()}_', '')
        v += [
            # user general overide.
            f'crud/{name}.html',
            f'crud/{mapped_name}.html',
            # Builtins
            f'trim/crud/{name}.html',
            f'trim/crud/{mapped_name}.html',
        ]
        return v

    def get_context_data(self, **kwargs):

        kwargs.setdefault('model_name', self.model.__name__)
        return super().get_context_data(**kwargs)


def extract_location(target):
    # appname == 'products'
    # mod_first == 'hyperlink'
    # name == 'Hyperlink'
    name = target.__name__
    mod_first = first_bit(name).lower()
    appname = first_bit(target.__module__)
    return (appname, mod_first, name,)


def create_class_slot(master_class, *additional_classes, **kwargs):
    _cls = (ShortMixin, master_class, ) + additional_classes
    return (_cls, (kwargs,{},), )


def first_bit(word):
    return word.split('.')[0]


def discover_models(target_name, models=None, module_needles=None):
    """
    trims.guess_classes(models=grab_models(models))
    trims.guess_classes()
    """

    if models is not None:
        return models

    no_needles = module_needles in (False, ALL, )
    needles = () if module_needles is None else module_needles
    keeps = ()

    model_name = first_bit(target_name)
    all_classes = apps.get_models(model_name)
    needles += (model_name,)

    for model in all_classes:
        module_name = first_bit(model.__module__)
        if no_needles or (module_name in needles):
            keeps += (model, )

    return keeps


def crud_classes(target_name=None, model_class=None, success_url=None,
                success_url_bit='list', models=None, module_needles=None,
                **base_definition):
    """
        return tuple(
                crud(m, target_name, success_url, success_url_bit, **base_definition)
                for m in ensure_tuple(model_class)
            )
    """
    r = ()
    if target_name is None:
        target_name = inspect.currentframe().f_back.f_globals['__name__']

    if model_class is None:
        model_class = discover_models(target_name, models, module_needles)

    model_class = ensure_tuple(model_class)

    for m in model_class:
        v = crud(m, class_module_name=target_name,
                 success_url=success_url,
                 success_url_bit=success_url_bit,
                 **base_definition)
        r += (v,)
    return r


def history_classes(target_name=None, model_class=None, models=None, class_module_name=None,
                    module_needles=None, **base_definition) -> tuple:
    """Generate a range of "history" class-based-views for the given `model_class`
    list. This is synonymous to calling `trim.views.history` repeatedly.

    Given a `model_class` as a `models.Model`, `list` or `tuple` type, build a
    set of Archive based views into the `target_name`.

    Arguments:
        **base_definition {dict} -- attributtes given to all classes as base
                                    class properties and methods

    Keyword Arguments:
        target_name {str} -- Name of the target module to insert the newly generated
            classes. If `None` the `__name__` of the calling method module
            is applied. (default: {None})
        model_class {models.Model, tuple, list} -- The target model or models
            to generate views. If `None` dicover the models using
            `trim.views.discover_models` (default: {None})
        models {list, tuple} -- Use an explicit list of `models` over `model_class`.
            If `None` the model_class is used (default: {None})
        class_module_name {str} -- The string name of the module to insert the
            newly generated classes, such as `"products.views"`.
            If `None` attempt to capture the _last frame_ caller module name,
            defaulting to the calling module name. (default: {None})
        module_needles {list, tuple} -- A list of module names to focus upon
            if model discovery is used. If a dicovered model originated from
            a module name within the needles, history views will be created
            (default: {None}).

    Returns:
        {tuple} -- A tuple of generated classes. The class-based-views already
                 exist within the `target_name`
    """

    if target_name is None:
        target_name = inspect.currentframe().f_back.f_globals['__name__']

    if model_class is None:
        model_class = discover_models(target_name, models, module_needles)

    model_class = ensure_tuple(model_class)

    r = ()
    for m in model_class:
        v = history(m, class_module_name=class_module_name or target_name,
                 **base_definition)
        r += (v,)
    return r


def crud(model, class_module_name=None, success_url=None, success_url_bit='list', **base_definition):
    """
        crud(models.Product)


        class ProductListView(ListView):
            model = models.Product

        class ProductCreateView(CreateView):
            model = models.Product
            fields = '__all__'


        class ProductUpdateView(UpdateView):
            model = models.Product
            fields = '__all__'


        class ProductDeleteView(DeleteView):
            model = models.Product
            success_url = reverse_lazy('products:list')


        class ProductDetailView(DetailView):
            model = models.Product


        same as:

            listview = gen_class(name, (ListView,), base_definition)
            createview = gen_class(name, (CreateView,), base_definition, **create_update_def)
            updateview = gen_class(name, (UpdateView,), base_definition, **create_update_def)
            detailview = gen_class(name, (DetailView,), base_definition)
            deleteview = gen_class(name, (DeleteView,), base_definition, **success_url_d)

        returns:

            return (
                listview,
                detailview,
                createview,
                updateview,
                deleteview,
            )
    """
    appname, mod_first, name = extract_location(model)

    lazy_url = success_url or f'{appname}:{mod_first}-{success_url_bit}'
    base_definition.setdefault('model', model)
    success_url_d = {'success_url': reverse_lazy(lazy_url)}
    create_update_def = {'fields':'__all__', **success_url_d}

    parts = (
        # Order is important here.
        # ( (ShortMixin, CreateView, ), (base_definition, create_update_def), ),
        ListView,
        (CreateView, create_update_def,),
        (UpdateView, create_update_def,),
        DetailView,
        (DeleteView, success_url_d),
    )

    return thin_parts_gen(parts, name, base_definition, class_module_name)


def history(model, class_module_name=None, **base_definition):
    """
        trims.history(models.Product, __name__, date_field='created')
    """

    if class_module_name is None:
        class_module_name = inspect.currentframe().f_back.f_globals['__name__']

    appname, mod_first, name = extract_location(model)
    base_definition.setdefault('model', model)
    base_definition.setdefault('date_field', 'created')

    parts = (
        ArchiveIndexView,
        DateDetailView,
        DayArchiveView,
        MonthArchiveView,
        TodayArchiveView,
        WeekArchiveView,
        YearArchiveView,
    )

    return thin_parts_gen(parts, name, base_definition, class_module_name)


def thin_parts_gen(parts, name, base_definition, class_module_name):
    packs = gen_thin_packs(parts, base_definition)
    return gen_packed_views(name, class_module_name, packs)


def gen_thin_packs(parts, base_definition):
    """
        parts = (
            # Order is important here.
            # ( (ShortMixin, CreateView, ), (base_definition, create_update_def), ),
            (ListView,),
            (CreateView, create_update_def,),
            (UpdateView, create_update_def,),
            (DetailView,),
            (DeleteView, success_url_d),
        )


        packs = (
            # Order is important here.
            # ( (ShortMixin, CreateView, ), (base_definition, create_update_def), ),
            create_class_slot(ListView, **base_definition),
            create_class_slot(CreateView, **base_definition, **create_update_def),
            create_class_slot(UpdateView, **base_definition, **create_update_def),
            create_class_slot(DetailView, **base_definition),
            create_class_slot(DeleteView, **base_definition, **success_url_d),
        )
    """
    packs = ()
    for part in parts:
        part = ensure_tuple(part)
        kw = part[1] if len(part) > 1 else {}
        slot = create_class_slot(part[0], **base_definition, **kw)
        packs += (slot, )
    return packs


def gen_packed_views(name, class_module_name, view_packs, master_class_position=1):
    """
        packs = (
            # Order is important here.
            # ( (ShortMixin, CreateView, ), (base_definition, create_update_def), ),
            create_class_slot(ListView, **base_definition),
            create_class_slot(CreateView, **base_definition, **create_update_def),
            create_class_slot(UpdateView, **base_definition, **create_update_def),
            create_class_slot(DetailView, **base_definition),
            create_class_slot(DeleteView, **base_definition, **success_url_d),
        )
    """

    r = ()
    for parents, definitions in view_packs:

        viewclass = gen_class(name, parents, definitions[0],
                              class_module_name=class_module_name,
                              master_class_position=master_class_position,
                              **definitions[1]
                              )
        r += (viewclass, )

    return r


def ensure_tuple(items):
    if isinstance(items, (list, tuple)) is False:
        items = (items,)
    return items


def gen_class(crud_name, crud_parents, class_definition, class_module_name=None,
              master_class_position=-1, **params):

    if class_module_name is None:
        class_module_name = __name__

    crud_parents = ensure_tuple(crud_parents)
    safe = params.pop('safe', True)

    parent_class_name = crud_parents[master_class_position].__name__
    view_class_name = params.pop('view_class_name', None)  or f"{crud_name}{parent_class_name}"
    module = sys.modules[class_module_name]

    view_cache[view_class_name] +=1

    if hasattr(module, view_class_name) is True and (safe is True):
        print('EXISTS', view_class_name)
        return getattr(module, view_class_name)

    class_members = copy_update(class_definition, **params)
    new_view_class = type(view_class_name, crud_parents, class_members)

    # print('Generating', view_class_name)
    setattr(module, view_class_name, new_view_class)

    return new_view_class


from collections import defaultdict
view_cache = defaultdict(int)

def copy_update(entity, **params):
    r = entity.copy()
    r.update(params)
    return r
