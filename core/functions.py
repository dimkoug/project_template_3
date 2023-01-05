from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_pagination(request, queryset, items):
    '''
    items: The number for pagination

    return tuple (paginator, total_pages, paginated queryset) 
    '''
    paginator = Paginator(queryset, items)
    page = request.GET.get('page')
    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
    return (paginator, paginator.num_pages, items_page)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def create_query_string(request):
    query_string = ''
    for key in request.GET.keys():
        if key != 'page':
            value = request.GET.getlist(key)
            if len(value) > 0:
                for item in value:
                    if value != '':
                        query_string += "&{}={}".format(key, item)
            else:
                if value != '':
                    query_string += "&{}={}".format(key, value)
    return query_string


def get_select_2_data(request):
    # example b2buser
    model_str = request.GET.get('model')
    # example b2b
    app_str = request.GET.get('app')
    q_objects = Q()
    d_objects = []
    q = request.GET.get('q')
    model = apps.get_model(app_label=app_str, model_name=model_str)
    for f in  model._meta.get_fields():
        print(f.__class__.__name__)
        if f.__class__.__name__  in ['CharField', 'TextField']:
            str_q = f"Q({f.name}__icontains=str({q}))"
            print(str_q)
            q_obj = eval(str_q)
            print(q_obj)
            q_objects |= q_obj

    data = model.objects.filter(q_objects)
    for d in data:
        d_objects.append({
            "id": d.pk,
            "title": d.__str__()
        })
    return JsonResponse(d_objects,safe=False)
