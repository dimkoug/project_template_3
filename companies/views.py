from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from companies.models import Company
from companies.forms import CompanyForm


# Create your views here.


class CompanyListView(ListView):
    model = Company
    queryset = Company.objects.prefetch_related('profiles')

    def dispatch(self, *args, **kwargs):
        self.ajax_partial = '{}/partials/{}_list_partial.html'.format(self.model._meta.app_label,self.model.__name__.lower())
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(profiles=self.request.user.profile)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = self.ajax_partial
        return context

class CompanyDetailView(DetailView):
    model = Company
    queryset = Company.objects.prefetch_related('profiles__user')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(profiles=self.request.user.profile)
        return queryset
    

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm


    def form_valid(self, form):
        obj = form.save()
        obj.profiles.add(self.request.user.profile)
        return super().form_valid(form)


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    queryset = Company.objects.prefetch_related('profiles')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(profiles=self.request.user.profile)
        return queryset


class CompanyDeleteView(DeleteView):
    model = Company
    queryset = Company.objects.prefetch_related('profiles')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(profiles=self.request.user.profile)
        return queryset