from django import forms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.forms import BootstrapForm


from companies.models import Company


def get_app_permissions(app_labels):
    """
    Retrieve permissions for specified apps.
    """
    permissions = Permission.objects.filter(content_type__app_label__in=app_labels)
    return permissions


class CompanyForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)


class PermissionSelectForm(BootstrapForm,forms.Form):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),  # Start with an empty queryset
        widget=forms.SelectMultiple,
        required=False,
        label="Select Permissions"
    )

    def __init__(self, *args, app_labels=None, **kwargs):
        super().__init__(*args, **kwargs)
        if app_labels:
            # Update the queryset with permissions for the specified apps
            self.fields['permissions'].queryset = get_app_permissions(app_labels)