from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str

from companies.models import Company
from profiles.models import Profile


User = get_user_model()


def get_company_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    model = Company
    q_objects = Q()
    d_objects = []
    search = request.GET.get('search')
    if search and search != '':
        for f in  model._meta.get_fields():
            if f.__class__.__name__  in ['CharField', 'TextField']:
                str_q = f"Q({f.name}__icontains=str('{search}'))"
                q_obj = eval(str_q)
                q_objects |= q_obj
        if request.user.is_superuser:
            data = model.objects.filter(q_objects)
        else:
            data = model.objects.prefetch_related('profiles').filter(q_objects,profiles=request.user.profile)
    else:
        if request.user.is_superuser:
            data = model.objects.all()
        else:
            data = model.objects.prefetch_related('profiles').filter(profiles=request.user.profile)
    
    
    for d in data:
        d_objects.append({
            "id": d.pk,
            "text": d.__str__()
        })
    return JsonResponse({"results": d_objects}, safe=False)





def activate_company_profile(request,company_id,user_id):
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


def remove_company_profile(request,company_id,profile_id):
    profile = Profile.objects.get(id=profile_id)
    company = Company.objects.get(id=company_id)
    company.profiles.remove(profile)
    return redirect(reverse("companies:company-detail",kwargs={"pk":company_id}))
