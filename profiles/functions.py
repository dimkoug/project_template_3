from django.db.models import Prefetch,Q
from django.http import JsonResponse
from profiles.models import Profile

def get_profiles_data(request):
    if request.user.is_anonymous:
        return JsonResponse({}, status=403)
    
    q_objects = Q()
    d_objects = []
    model = Profile
    search = request.GET.get('search', '').strip()
    
    if search:
        for f in model._meta.get_fields():
            field_name = f.name
            field_class_name = f.__class__.__name__

            # Direct CharField or TextField search
            if field_class_name in ['CharField', 'TextField', 'FileField']:
                q_obj = Q(**{f"{field_name}__icontains": search})
                q_objects |= q_obj
            
            # ForeignKey search on related model's CharField or TextField fields
            elif field_class_name == 'ForeignKey':
                # Get the related model
                related_model = f.related_model
                for related_field in related_model._meta.get_fields():
                    if related_field.__class__.__name__ in ['CharField', 'TextField']:
                        q_obj = Q(**{f"{field_name}__{related_field.name}__icontains": search})
                        q_objects |= q_obj
        
        # Filter data based on the search query
        data = model.objects.filter(q_objects)
    else:
        # Retrieve all data if no search query is provided
        data = model.objects.all()
    

    
    # Prepare response data
    for document in data:
        d_objects.append({
            "id": document.pk,
            "text": str(document)  # Using str() to avoid potential issues with custom __str__
        })
    
    return JsonResponse({"results": d_objects}, safe=False)