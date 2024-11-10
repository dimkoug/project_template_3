from django import forms
from invitations.models import Invitation
from core.widgets import *

from companies.models import Company


from core.forms import BootstrapForm


class InvitationForm(BootstrapForm, forms.ModelForm):
    company = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/companies/sb/'),required=False,queryset=Company.objects.none())
    class Meta:
        model = Invitation
        fields = ('email','company')


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        company_queryset = Company.objects.none()
        if 'company' in self.data:
            if not self.request.user.is_superuser:
                company_queryset = Company.objects.prefetch_related('profiles').filter(profiles=self.request.user.profile)
            else:
                company_queryset = Company.objects.prefetch_related('profiles').all()
        if self.instance.pk:
            if self.request.user.is_superuser:
                company_queryset = Company.objects.filter(id=self.instance.company_id)
            else:
                company_queryset = Company.objects.prefetch_related('profiles').filter(id=self.instance.company_id,profiles__in=self.request.user.profile.id)


        self.fields['company'].queryset = company_queryset
        self.fields['company'].widget.queryset = company_queryset