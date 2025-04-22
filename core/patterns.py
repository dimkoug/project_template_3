from importlib import import_module
from django.apps import apps
from django.urls import path
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def get_patterns(app_name, filename):
    app_module = import_module('{}.{}'.format(app_name, filename))
    app_models = apps.get_app_config(app_name).get_models()
    model_names = [model.__name__ for model in app_models]
    patterns = []
    views = []

    for model in model_names:
        for key, value in app_module.__dict__.items():
            if isinstance(value, type):
                if value.__name__.startswith(model):
                    views.append({key: value})
    _views = set()
    for key in views:
        for key, value in key.items():
            for model_name in model_names:
                if value.__name__.startswith(model_name) and\
                            value.__name__ not in _views:
                    
                    if isinstance(value, type):
                        
                        
                        if issubclass(value, ListView):
                            patterns += [path('{}/'.format(
                                model_name.lower()), value.as_view(),
                                name=f'{model_name.lower()}_list')]
                        if issubclass(value, DetailView):
                            if value.pk_url_kwarg == 'pk':
                                key = f"<int:{value.pk_url_kwarg}>"
                            else:
                                key = f"<str:{value.pk_url_kwarg}>"
                            
                            
                            
                            patterns += [path(f'{model_name.lower()}/view/{key}/', value.as_view(),
                                name=f'{model_name.lower()}_view')]
                        if issubclass(value, CreateView):
                            patterns += [path('{}/add/'.format(
                                model_name.lower()), value.as_view(),
                                name=f'{model_name.lower()}_add')]
                        if issubclass(value, UpdateView):
                            if value.pk_url_kwarg == 'pk':
                                key = f"<int:{value.pk_url_kwarg}>"
                            else:
                                key = f"<str:{value.pk_url_kwarg}>"
                            
                            patterns += [path(f'{model_name.lower()}/change/{key}/', value.as_view(),
                                name=f'{model_name.lower()}_change')]
                        if issubclass(value, DeleteView):
                            if value.pk_url_kwarg == 'pk':
                                key = f"<int:{value.pk_url_kwarg}>"
                            else:
                                key = f"<str:{value.pk_url_kwarg}>"
                            
                            
                            patterns += [path(f'{model_name.lower()}/delete/{key}/', value.as_view(),
                                name=f'{model_name.lower()}_delete')]
            _views.add(value.__name__)

    return patterns
