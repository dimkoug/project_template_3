from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from core.functions import get_rows 

from .functions import create_query_string, is_ajax


class FormInvalidMixin:
    def form_invalid(self, form, **kwargs):
        from django.contrib import messages
        messages.error(self.request, f"{self.model.__name__.capitalize()} not saved.")
        for field in form.errors:
            try:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            except KeyError:
                form[field].field.widget.attrs['class'] = ' is-invalid'
        if is_ajax(self.request):
            return JsonResponse(form.errors, safe=False, status=400)
        return super().form_invalid(form)



class AjaxMixin:
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except:
            self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        class_name = self.__class__.__name__.lower()
        if 'list' in class_name:
            name = '_list_partial.html'
        elif 'detail' in class_name:
            name = '_detail_partial.html'
        elif 'delete' in class_name:
            name = '_confirim_delete_partial.html'
        print(name)
        self.ajax_partial = f"{self.model._meta.app_label}/partials/{self.model.__name__.lower()}{name}"
        context['template'] = self.ajax_partial
        if is_ajax(request):
            print(self.ajax_partial)
            template = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse({'template': template})
        return self.render_to_response(context)

class QueryListMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        q_objects = Q()
        if q and q != '':
            q = str(q.strip())
            for f in  self.model._meta.get_fields():
                print(f.__class__.__name__)
                if f.__class__.__name__  in ['CharField', 'TextField']:
                    str_q = f"Q({f.name}__icontains='{q}')"
                    print(str_q)
                    q_obj = eval(str_q)
                    print(q_obj)
                    q_objects |= q_obj
            queryset = queryset.filter(q_objects)
        return queryset



class ModelMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        model = self.model
        app = model._meta.app_label
        model_name = model.__name__.lower()
        title = model._meta.verbose_name_plural.capitalize()
        back_url = reverse("{}:{}-list".format(app, model_name))
        create_url = reverse("{}:{}-create".format(app, model_name))
        context['app'] = app
        context['model'] = model
        context['model_name'] = model_name
        context['back_url'] = back_url
        context['create_url'] = create_url
        context['page_title'] = title
        context['query_string'] = create_query_string(self.request)
        return context


class AjaxListMixin:
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if is_ajax(request):
            data = serializers.serialize("json", self.object_list)
            return JsonResponse(data, safe=False)
        context = self.get_context_data()
        return self.render_to_response(context)


class AjaxFormMixin:
    def form_valid(self, form):
        form.save()
        if is_ajax(self.request):
            data = serializers.serialize("json", [form.instance])
            return JsonResponse(data, safe=False, status=200)
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        from django.contrib import messages
        messages.error(self.request, f"{self.model.__name__.capitalize()} not saved.")
        for field in form.errors:
            try:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            except KeyError:
                form[field].field.widget.attrs['class'] = ' is-invalid'
        if is_ajax(self.request):
            return JsonResponse(form.errors, safe=False, status=400)
        return super().form_invalid(form)
    




class FormMixin:
    def form_valid(self, form):
        if 'continue' in self.request.POST:
            form.save()
            return redirect(reverse_lazy('{}:{}-update'.format(
                form.instance._meta.app_label,
                form.instance.__class__.__name__.lower()),
                kwargs={'pk': form.instance.pk}))
        if 'new' in self.request.POST:
            form.save()
            return redirect(reverse_lazy('{}:{}-create'.format(
                form.instance._meta.app_label,
                form.instance.__class__.__name__.lower())))
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        from django.contrib import messages
        messages.error(self.request, f"{self.model.__name__.capitalize()} not saved.")
        for field in form.errors:
            try:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            except KeyError:
                form[field].field.widget.attrs['class'] = ' is-invalid'
        if is_ajax(self.request):
            return JsonResponse(form.errors, safe=False, status=400)
        return super().form_invalid(form)


class SuccessUrlMixin:
    def get_success_url(self):
        return reverse_lazy('{}:{}-list'.format(
            self.model._meta.app_label, self.model.__name__.lower()))


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PaginationMixin:

    def get_paginate_by(self, queryset):
        # Check for page size in URL query parameters
        page_size = self.request.GET.get('page_size')
        if page_size:
            return int(page_size)
        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]
        
        try:
            context['fields'] = self.fields
            table = get_rows(self.fields,current_page)
            context['table'] = table
        except:
            raise
        context.update({'pages': pages})
        return context


class AjaxDeleteMixin:
    def dispatch(self, *args, **kwargs):
        self.app = self.model._meta.app_label
        self.model_name = self.model.__name__.lower()
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        if is_ajax(self.request):
            self.object = self.get_object()
            self.object.delete()
            data = dict()
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            return self.delete(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if is_ajax(request):
            html_form = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse({'html_form': html_form})
        return super().get(request, *args, **kwargs)
