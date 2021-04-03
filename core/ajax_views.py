from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.views import CoreListView, CoreDetailView, CoreCreateView, CoreUpdateView, CoreDeleteView
from core.mixins import AjaxCreateMixin,AjaxUpdateMixin,AjaxDeleteMixin, PassRequestToFormViewMixin, ModelMixin


class CoreAjaxCreateView(LoginRequiredMixin, AjaxCreateMixin,
                         PassRequestToFormViewMixin,
                         ModelMixin, CreateView):
    pass

class CoreAjaxUpdateView(LoginRequiredMixin, AjaxUpdateMixin,
                         PassRequestToFormViewMixin,
                         ModelMixin, UpdateView):
    pass

class CoreAjaxDeleteView(LoginRequiredMixin, AjaxDeleteMixin,
                         PassRequestToFormViewMixin,
                         ModelMixin, DeleteView):
    pass
