import datetime
from decimal import Decimal
from django import template
from django.urls import reverse,reverse_lazy, NoReverseMatch, resolve
from django.apps import apps
from django.db.models.fields.files import ImageFieldFile, FileField
from django.utils.html import format_html
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag(takes_context=True)
def get_url(context, action, obj=None):
    '''
    example 1  " get_url 'list' "
    example 2  " get_url 'create' "
    example 3  " get_url 'detail' obj  "
    the first argument is action create or list or detail or update or delete
    the second argument is a model object
    the name of url pattern so as to work
    app:model-create
    app:model-update
    app:model-delete
    app:model-detail
    '''
    if not obj:
        model = context['model']
        lower_name = model.__name__.lower()
        app = model._meta.app_label
    else:
        model = obj
        lower_name = model.__class__.__name__.lower()
        app = model._meta.app_label

    url_string = '{}:{}-{}'.format(app, lower_name, action)
    if obj:
       try:
           url = reverse(url_string, kwargs={'pk': obj.pk})
       except NoReverseMatch:
           url = reverse(url_string, kwargs={'slug': obj.slug})
    if not obj:
        url_string = '{}:{}-{}'.format(app, lower_name, action)
        url = reverse_lazy(url_string)
    return url


@register.simple_tag(takes_context=True)
def get_template_name(context, *args):
    model = context['model']
    template_name = context['template']
    app = model._meta.app_label
    template_name = f"{app}/partials/{template_name}"
    return template_name

def sortFn(value):
  return value.__name__


@register.simple_tag(takes_context=True)
def get_generate_sidebar(context):
    request = context['request']
    urls = ""
    app_models = list(apps.get_app_config(context['app']).get_models())
    app_models.sort(key=sortFn)
    
    for model in app_models:
        try:
            url_item = reverse(
                "{}:{}-list".format(model._meta.app_label, model.__name__.lower()))
        except NoReverseMatch:
            url_item = None
        if url_item:
            item = "<div><a href='{}'".format(url_item)
            if url_item == request.path:
                item += "class='active'"
            item += ">{}</a></div>".format(model._meta.verbose_name_plural.capitalize())
            print(item)
            urls += item
    return format_html(mark_safe(urls))


@register.simple_tag
def get_boolean_img(value):
    if value:
        return format_html(mark_safe('<i class="bi bi-check-lg"></i>'))
    return format_html(mark_safe('<i class="bi bi-x"></i>'))


@register.simple_tag
def get_model_name(obj):
    if obj:
        try:
            return obj.__class__.__name__.lower()
        except:
            return obj.__name__.lower()

    return ''


@register.simple_tag
def get_model_app(obj):
    if obj:
        return obj._meta.app_label
    return ''


@register.simple_tag
def get_formset_img(obj, value):
    if value.__class__.__name__ == 'ImageFieldFile' and value:
        return format_html(mark_safe('<img src="{}" width="100px" />'.format(value.url)))
    return ""


@register.simple_tag
def is_active(request , url):
    if  resolve(request.path).url_name == url:
        return 'active'
    return ''



@register.simple_tag
def get_rows(fields, object_list):
    trs = []
    for obj in object_list:
        app = obj._meta.app_label
        model = obj.__class__.__name__.lower()
        update_url = reverse_lazy(f"{app}:{model}-update",kwargs={"pk":obj.pk})
        delete_url = reverse_lazy(f"{app}:{model}-delete",kwargs={"pk":obj.pk})
        tr = '<tr>'
        for field in fields:
            db_name = field['db_name']
            value = getattr(obj, db_name)
            print(value.__class__.__name__)
            if isinstance(value, Decimal):
                value = round(value,0)
            if isinstance(value, bool):
                if value:
                    value = format_html(mark_safe('<i class="bi bi-check-lg text-success"></i>'))
                else:
                    value = format_html(mark_safe('<i class="bi bi-x-lg text-danger"></i>'))
            if isinstance(value,ImageFieldFile):
                if value and value.url:
                    value = format_html(mark_safe('<img src="{}" width="100px" />'.format(value.url)))
            tr += '<td>' + str(value) + '</td>'
        tr += f"""<td><a href='{update_url}'>{format_html(mark_safe('<i class="bi bi-pencil-square text-warning" style="font-size:1.5rem;"></i>'))}</a><a href='{delete_url}        'class='delete-tr'>{format_html(mark_safe('<i class="bi bi-x text-danger" style="font-size:1.5rem;"></i>'))}</a></td>"""
        
        tr += '</tr>'
        trs.append(tr)
    items = ''
    for i in trs:
        items += str(i)
    return format_html(mark_safe(items))


@register.inclusion_tag("core/add_button.html",takes_context=True)
def add_button(context):
    view = context["view"]
    model = view.model
    url = reverse(f"{model._meta.app_label}:{model.__name__.lower()}-create")
    return {"url":url}


@register.inclusion_tag("core/title.html",takes_context=True)
def get_title(context):
    view = context["view"]
    model = view.model
    return {"title":model._meta.verbose_name_plural.capitalize()}


@register.inclusion_tag("core/actions.html",takes_context=True)
def get_actions(context, obj):
    view = context["view"]
    model = view.model
    change_url = reverse(f"{model._meta.app_label}:{model.__name__.lower()}-update",kwargs={"pk":obj.pk})
    delete_url = reverse(f"{model._meta.app_label}:{model.__name__.lower()}-delete",kwargs={"pk":obj.pk})
    return {"change_url":change_url,"delete_url":delete_url}


@register.simple_tag(takes_context=True)
def get_list_url(context, form):
    try:
        model = form.instance
        list_url = reverse(f"{model._meta.app_label}:{model.__class__.__name__.lower()}-list")
    except:
        model = context['view'].model
        list_url = reverse(f"{model._meta.app_label}:{model.__name__.lower()}-list")
    
    return list_url


@register.simple_tag(takes_context=True)
def get_change_url(context, obj):
    view = context["view"]
    model = view.model
    change_url = reverse(f"{model._meta.app_label}:{model.__name__.lower()}-update",kwargs={"pk":obj.pk})
    delete_url = reverse(f"{model._meta.app_label}:{model.__name__.lower()}-delete",kwargs={"pk":obj.pk})
    return change_url

@register.simple_tag
def get_delete_url(form):
    model = form.instance
    delete_url = reverse(f"{model._meta.app_label}:{model.__class__.__name__.lower()}-delete",kwargs={"pk":form.instance.pk})
    return delete_url


@register.inclusion_tag("core/form_buttons.html",takes_context=True)
def get_form_buttons(context, form):
    return {"form":form, "context":context}


@register.simple_tag
def display_data(object):
    items = {}
    for field in object._meta.fields:
        print(type(field), field.name)
        value = getattr(object,field.name)
        if isinstance(value, Decimal):
            value = round(value,0)
        if isinstance(value, datetime.datetime):
            format = '%Y-%m-%d %H:%M:%S'
            print(format)
            # applying strftime() to format the datetime
            string = value.strftime(format)
            value = str(string)
        items[field.name] = value
    return items
