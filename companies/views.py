from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from companies.models import Company
from companies.forms import CompanyForm

from core.functions import create_query_string, is_ajax
from core.mixins import PaginationMixin,SuccessUrlMixin, QueryMixin
# Create your views here.


class CompanyListView(PaginationMixin,QueryMixin,ListView):
    model = Company
    paginate_by = 2
    fields = {}
    queryset = Company.objects.prefetch_related('profiles')
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if is_ajax(request):
            html_form = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse(html_form, safe=False)
        return super().get(request, *args, **kwargs)

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
        context['search'] = self.request.GET.get('search','')
        return context

class CompanyDetailView(DetailView):
    model = Company
    queryset = Company.objects.prefetch_related('profiles__user')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(profiles=self.request.user.profile)
        return queryset
    

class CompanyCreateView(SuccessUrlMixin,CreateView):
    model = Company
    form_class = CompanyForm


    def form_valid(self, form):
        obj = form.save()
        obj.profiles.add(self.request.user.profile)
        return super().form_valid(form)


class CompanyUpdateView(SuccessUrlMixin,UpdateView):
    model = Company
    form_class = CompanyForm
    queryset = Company.objects.prefetch_related('profiles')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(profiles=self.request.user.profile)
        return queryset


class CompanyDeleteView(SuccessUrlMixin,DeleteView):
    model = Company
    queryset = Company.objects.prefetch_related('profiles')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(profiles=self.request.user.profile)
        return queryset