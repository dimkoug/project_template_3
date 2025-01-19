from django import forms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from core.forms import BootstrapForm


from companies.models import Company
from django.db.models import Prefetch
from profiles.models import Profile
from core.widgets import CustomSelectMultipleWithUrl, CustomSelectWithQueryset
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
            

class CompanyFieldMixin(BootstrapForm, forms.ModelForm):
    company = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/companies/sb/'),required=False,queryset=Company.objects.none())

    class Meta:
        abstract = True  # This makes it an abstract base class

    def __init__(self,request,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = request.user
        user_profile = user.profile
        print(user.profile.companies.all())
        queryset = Company.objects.prefetch_related(
            Prefetch(
                'profiles',
                queryset=Profile.objects.filter(user=request.user),
                to_attr='user_profiles'
            )
        ).filter(profiles=request.user.profile)
        if 'company' in self.data:
            if user.is_superuser:
                queryset = Company.objects.all()
            else:
                queryset = Company.objects.prefetch_related(
                Prefetch(
                    'profiles',
                    queryset=Profile.objects.filter(user=request.user),
                    to_attr='user_profiles'
                )
            ).filter(profiles__in=request.user.profile)
        elif self.instance.pk:
            if user.is_superuser:
                queryset = self.instance.companies.all()
            else:
                queryset = Company.objects.prefetch_related(
                Prefetch(
                    'profiles',
                    queryset=Profile.objects.filter(user=request.user),
                    to_attr='user_profiles'
                )
            ).filter(profiles=request.user.profile,id=self.instance.company_id)
        print(queryset)
        self.fields['company'].queryset = queryset