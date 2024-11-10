from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    AuthenticationForm as BaseAuthenticationForm,
    PasswordResetForm as BasePasswordResetForm,
    UserCreationForm as BaseUserCreationForm,
    SetPasswordForm as BaseSetPasswordForm,
)

from core.forms import BootstrapForm

User = get_user_model()


class UserCreationForm(BootstrapForm, BaseUserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    company = forms.CharField(max_length=255, required=False)
    class Meta:
        model = User
        fields = ('email', 'birth_date', 'password1', 'password2', )

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super().__init__(*args, **kwargs)
    #     sign_type = self.request.GET.get('type')
    #     if sign_type == 'user':
    #         self.fields.pop('company')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        signup_type = self.request.GET.get('type')
        email = self.request.session.get('email')
        print(signup_type)
        if (signup_type and signup_type == 'user') or email:
            self.fields.pop('company')
        else:
            self.fields['company'] = forms.CharField(max_length=254, help_text='Add your company')
            self.fields['company'].widget.attrs.update({
                    'class': 'form-control'
            })





class UserAuthenticationForm(BootstrapForm, BaseAuthenticationForm):
    pass


class UserPasswordResetForm(BootstrapForm, BasePasswordResetForm):
    pass


class UserSetPasswordForm(BootstrapForm, BaseSetPasswordForm):
    pass
