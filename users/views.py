from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_str as force_text

from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.views.generic import FormView
from django.conf import settings
from companies.models import Company
from profiles.models import Profile

from users.tokens import account_activation_token
from users.forms import (
    UserCreationForm, UserAuthenticationForm,
    UserPasswordResetForm
)
User = get_user_model()


class LoginView(auth_views.LoginView):
    form_class = UserAuthenticationForm


class LogoutView(auth_views.LogoutView):
    pass


class PasswordResetView(auth_views.PasswordResetView):
    form_class = UserPasswordResetForm


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    pass


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    pass


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    pass


class AccountActivationSent(TemplateView):
    template_name = 'registration/account_activation_sent.html'


class SignupTypeView(TemplateView):
    template_name = 'registration/signup_type.html'


class PendingActivationView(TemplateView):
    template_name = 'registration/pending_activation.html'


class SignupView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get_initial(self):
        initial = super().get_initial()
        if 'email' in self.request.session:
            initial.update({
                'email': self.request.session['email']
            })
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(self.request)
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            signup_type = self.request.GET.get('type')
            if signup_type == 'company':
                company, created = Company.objects.get_or_create(name=self.request.POST['company'])
                company.profiles.add(user.profile)
                company.refresh_from_db()
                if created and company.profiles.count() == 1:
                    group, cr = Group.objects.get_or_create(name=f"{company.name}_{settings.ADMIN_GROUP}")
                    content_type = ContentType.objects.get_for_model(Company)
                    permissions = Permission.objects.filter(
                            content_type=content_type,
                            codename__in=['add_company', 'change_company', 'delete_company', 'view_company']
                    )
                    group.permissions.add(*permissions)

                    user.groups.add(group)
                    user.is_active = True
                    user.profile.email_confirmed = True
                    user.save()
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    group, cr = Group.objects.get_or_create(name=f"{company.name}_{settings.USERS_GROUP}")
                    content_type = ContentType.objects.get_for_model(Company)
                    permissions = Permission.objects.filter(
                            content_type=content_type,
                            codename__in=['view_company']
                    )
                    group.permissions.add(*permissions)
                    user.groups.add(group)
                    user.is_active = False
                    user.profile.email_confirmed = False
                    user.save()
                    return redirect('pending_activation')
            else:
                group, cr = Group.objects.get_or_create(name=f"{settings.USERS_GROUP}")
                user.groups.add(group)
                user.save()
            
            if not 'company' in self.request.session:  
                subject = 'Activate Your MySite Account'
                message = render_to_string('registration/account_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                return redirect('account_activation_sent')
            else:
                company = Company.objects.get(name=self.request.session.get('company'))
                user.is_active = True
                user.profile.email_confirmed = True
                parent = Profile.objects.get(id=int(self.request.session.get('parent')))
                user.parent = parent.user
                user.profile.parent = parent
                user.save()
                company.profiles.add(user.profile)
                company.save()
                group, cr = Group.objects.get_or_create(name=f"{company.name}_{settings.USERS_GROUP}")
                content_type = ContentType.objects.get_for_model(Company)
                permissions = Permission.objects.filter(
                        content_type=content_type,
                        codename__in=['view_company']
                )
                group.permissions.add(*permissions)
                user.groups.add(group)
                user.save()
                user.refresh_from_db()
                login(self.request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

        return super().form_valid(form)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return render(request, 'registration/account_activation_invalid.html')
