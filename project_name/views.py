from django.views.generic import TemplateView

from core.mixins import ProtectedViewMixin


class HomeView(TemplateView):
    template_name = "index.html"


class ManageView(ProtectedViewMixin, TemplateView):
    template_name = "manage.html"
