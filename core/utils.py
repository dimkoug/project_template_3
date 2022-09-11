from django.apps import apps
from django.http import JsonResponse

def delete_item(request):
    id = request.GET.get('id')
    if not id:
        return JsonResponse({}, safe=False)
    model = request.GET.get('model')
    app = request.GET.get('app')
    model_obj = apps.get_model(app_label=app, model_name=model)
    model_obj.objects.get(id=id).delete()
    return JsonResponse({'message': 'deleted'}, safe=False)