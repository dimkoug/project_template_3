import json
from django.apps import apps
from django.http import JsonResponse, HttpResponse

from .functions import is_ajax

def delete_item(request):
    id = request.GET.get('id')
    if not id:
        return JsonResponse({}, safe=False)
    model = request.GET.get('model')
    app = request.GET.get('app')
    model_obj = apps.get_model(app_label=app, model_name=model)
    model_obj.objects.get(id=id).delete()
    return JsonResponse({'message': 'deleted'}, safe=False)


def model_order(request):
    if request.method == 'POST' and is_ajax(request):
        model_name = request.POST['model_name']
        app_name = request.POST['app_name']
        model = apps.get_model(app_name, model_name)

        # Parse the JSON string
        page_id_array = json.loads(request.POST.get('page_id_array', '[]'))

        objs = []
        for index, item in enumerate(page_id_array):
            print(item)
            obj = model.objects.get(pk=item)
            obj.order = index
            objs.append(obj)
        model.objects.bulk_update(objs, ['order'])
        return JsonResponse(page_id_array, safe=False)
    return HttpResponse('')