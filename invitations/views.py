from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView 
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import login,logout
from core.views import *
from core.mixins import BaseListMixin,BaseDetailMixin,BaseCreateMixin,BaseUpdateMixin,BaseDeleteMixin


from invitations.models import Invitation
from invitations.forms import InvitationForm

from users.tokens import account_activation_token

class InvitationListView(BaseListView):
    model = Invitation
    paginate_by = 2

    queryset = Invitation.objects.prefetch_related('company__profiles').select_related('user')


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class InvitationDetailView(BaseDetailView):
    model = Invitation
   
    queryset = Invitation.objects.prefetch_related('company__profiles').select_related('user')


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class InvitationCreateView(BaseCreateView):
    model = Invitation
    form_class = InvitationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

    def form_valid(self,form):
        form.instance._logged_user = self.request.user
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        current_site = get_current_site(self.request)
        data = {
            'email': obj.email,
            'user': obj.user.email,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(obj.pk)),
            'token': account_activation_token.make_token(obj.user),
        }
        msg_plain = render_to_string('registration/invitation.txt', data)
        msg_html = render_to_string('registration/invitation.html', data)
        send_mail(
            'email title',
            msg_plain,
            'some@sender.com',
            ['some@receiver.com'],
            html_message=msg_html,
        )
        return super().form_valid(obj)
   


class InvitationUpdateView(BaseUpdateView):
    model = Invitation
    form_class = InvitationForm

    queryset = Invitation.objects.prefetch_related('company__profiles').select_related('user')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
   


class InvitationDeleteView(BaseDeleteView):
    model = Invitation

    queryset = Invitation.objects.prefetch_related('company__profiles').select_related('user')


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset