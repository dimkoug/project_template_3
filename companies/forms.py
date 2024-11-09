from django import forms

from core.forms import BootstrapForm


from companies.models import Company


class CompanyForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)