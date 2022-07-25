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
