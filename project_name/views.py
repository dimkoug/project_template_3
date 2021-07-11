from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = "site/index.html"


class ManageView(LoginRequiredMixin, TemplateView):
    template_name = "cms/manage.html"
