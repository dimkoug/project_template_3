from typing import Any
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView



from companies.models import Company
from companies.forms import CompanyForm, PermissionSelectForm

User = get_user_model()

# Create your views here.


def assign_permissions(request, company_id, user_id):
    user = User.objects.get(id=user_id)
    app_labels = [app for app in settings.INSTALLED_APPS   if 'django' not in app]  # List the specific app labels here

    if request.method == 'POST':
        form = PermissionSelectForm(request.POST, app_labels=app_labels)
        if form.is_valid():
            # Clear existing permissions
            user.user_permissions.clear()
            
            # Add selected permissions
            user.user_permissions.set(form.cleaned_data['permissions'])
            
            return redirect(reverse('companies:company-detail', kwargs={"pk":company_id}))  # Redirect after successful save
    else:
        form = PermissionSelectForm(app_labels=app_labels)
    
    return render(request, 'companies/assing_permissions.html', {'form': form, 'user': user})



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