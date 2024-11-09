from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str

from companies.models import Company
from profiles.models import Profile
from users.models import User




def activate_profile(request,company_id,user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    current_site = get_current_site(request)
    data = {
        'email': user.email,
        'user': user.email,
        'domain': current_site.domain,
    }
    msg_plain = render_to_string('registration/activated_account.txt', data)
    msg_html = render_to_string('registration/activated_account.html', data)
    send_mail(
        'email title',
        msg_plain,
        'some@sender.com',
        ['some@receiver.com'],
        html_message=msg_html,
    )
    return redirect(reverse("companies:company-detail",kwargs={"pk":company_id}))


def remove_profile(request,company_id,profile_id):
    profile = Profile.objects.get(id=profile_id)
    company = Company.objects.get(id=company_id)
    company.profiles.remove(profile)
    return redirect(reverse("companies:company-detail",kwargs={"pk":company_id}))
