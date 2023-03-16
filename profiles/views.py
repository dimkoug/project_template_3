from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
# Create your views here.

from .forms import ProfileForm
from .models import Profile


class ProtectProfile:
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.pk != self.get_object().pk:
            raise PermissionDenied()
        return super().dispatch(*args, **kwargs)


class ProfileDetailView(ProtectProfile, LoginRequiredMixin, DetailView):
    model = Profile

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        uuid = urlsafe_base64_encode(force_bytes(self.get_object().pk))
        token = default_token_generator.make_token(self.get_object().user)
        url = self.request.build_absolute_uri(reverse(
                        "password_reset_confirm",
                        kwargs={"uidb64": uuid, "token": token}))
        context['password_url'] = url
        return context


class ProfileUpdateView(ProtectProfile, LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile-detail',
                            kwargs={'pk': self.get_object().pk})


class ProfileDeleteView(ProtectProfile, LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'profiles/profile_confirm_delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile-detail',
                            kwargs={'pk': self.get_object().pk})
