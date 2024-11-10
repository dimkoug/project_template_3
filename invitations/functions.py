
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout
from companies.models import Company
from invitations.models import Invitation
from users.tokens import account_activation_token
User = get_user_model()



def activate_invite(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        invitation = Invitation.objects.select_related('company').get(pk=uid)
    except (TypeError, ValueError, OverflowError, Invitation.DoesNotExist):
        invitation = None

    if invitation is not None and account_activation_token.check_token(invitation.user, token):
        try:
            user = User.objects.get(email=invitation.email)
        except:
            user = None
        if user:
            company = Company.objects.get(name=invitation.company.name)
            company.profiles.add(user.profile)
            login(request,user)
            return redirect('index')
        
        request.session['email'] = invitation.email
        request.session['company'] = invitation.company.name
        request.session["parent"] = invitation.user.profile.id
        url = reverse_lazy('signup')
        return redirect(url)
    else:
        return render(request, 'registration/invitation_invalid.html')
    


def resend_invitation(request,invitation_id):
    invitation = Invitation.objects.select_related('user').get(id=invitation_id)
    current_site = get_current_site(request)
    data = {
        'email': invitation.email,
        'user': invitation.user.email,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(invitation.pk)),
        'token': account_activation_token.make_token(invitation.user),
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
    return redirect(reverse_lazy('invitations:invitation-list'))
