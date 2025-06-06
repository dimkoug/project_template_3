import uuid
import os
import hashlib
import datetime
import importlib
from urllib.parse import unquote
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models import Q
from django.urls import reverse_lazy
from django.db import models
from django.utils.html import format_html, mark_safe
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

User = get_user_model()


class Url(models.Model):
    class Meta:
        abstract = True

    def get_view_class(self, klass,action):
        """
        Dynamically import the view based on naming convention:
        `{AppLabel}.views.{ModelName}{Action}View`
        """
        app = self._meta.app_label
        model = self.__class__.__name__
        view_class_name = f"{model}{klass.capitalize()}View"
        try:
            views_module = importlib.import_module(f"{app}.views")
            return getattr(views_module, view_class_name)
        except (ModuleNotFoundError, AttributeError):
            return None

    def get_url(self, klass, action):
        view_class = self.get_view_class(klass,action)
        if not view_class:
            return ""

        pk_kwarg = getattr(view_class, "pk_url_kwarg", "pk")
        print(pk_kwarg)
        pk_value = getattr(self, pk_kwarg, None)
        print(pk_value)
        if pk_value is None:
            return ""

        return reverse_lazy(
            f"{self._meta.app_label}:{self.__class__.__name__.lower()}_{action}",
            kwargs={pk_kwarg: pk_value}
        )

    @property
    def get_view_url(self):
        return self.get_url("detail","view")

    @property
    def get_change_url(self):
        return self.get_url("update","change")

    @property
    def get_delete_url(self):
        return self.get_url("delete","delete")




class UserData(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="%(app_label)s_%(class)s_user_created")
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="%(app_label)s_%(class)s_user_updated")

    class Meta:
        abstract = True


class UnicodeUrl(models.Model):
    class Meta:
        abstract = True

    def get_unicode_url(self):
        url = self.get_absolute_url()
        return unquote(url)


class Ordered(models.Model):
    order = models.PositiveIntegerField(default=0,db_index=True)

    class Meta:
        abstract = True


class Timestamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Seo(models.Model):
    meta_description = models.TextField(
                                        help_text="Seo description",
                                        null=True, blank=True)
    meta_keywords = models.CharField(max_length=200,
                                     help_text="Comma separated keywords for page",
                                     null=True, blank=True)
    class Meta:
        abstract = True


class UUidModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


class ConfigurableSlugModel(models.Model):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        self.slug_source_field = getattr(self, 'SLUG_SOURCE_FIELD', 'name')
        self.slug_field = getattr(self, 'SLUG_FIELD', 'slug')
        super().__init__(*args, **kwargs)

    def clean(self):
        source_value = getattr(self, self.slug_source_field)
        if source_value:
            proposed_slug = slugify(source_value)
            model_class = self.__class__
            exists = model_class.objects.filter(
                Q(**{self.slug_field: proposed_slug}) &
                ~Q(pk=self.pk if self.pk else None)
            ).exists()

            if exists:
                raise ValidationError({
                    self.slug_source_field: _('An entry with this slug already exists.')
                })

    def save(self, *args, **kwargs):
        source_value = getattr(self, self.slug_source_field)
        if source_value:
            setattr(self, self.slug_field, slugify(source_value))
        self.full_clean()
        super().save(*args, **kwargs)


class Published(models.Model):
    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


class MediaFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise(Exception("name's length is greater than max_length"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(MediaFileSystemStorage, self)._save(name, content)


def get_upload_path(instance, filename):
    name = instance.__class__.__name__.lower()
    return os.path.join('{}_{}_{}/{}/{}'.format(
        datetime.datetime.now().day,
        datetime.datetime.now().month,
        datetime.datetime.now().year, name, filename))


class Media(models.Model):
    image = models.ImageField(upload_to=get_upload_path,
                              storage=MediaFileSystemStorage(), null=True, blank=True)
    caption = models.CharField(null=True, blank=True, max_length=100)
    md5sum = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        abstract = True

    def filename(self):
        return os.path.basename(self.image.name)



    def get_thumb(self):
        if self.image:
            return format_html("<img src='{}' width='100' height='auto'>",
                               self.image.url)
        return ''

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.image.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super().save(*args, **kwargs)
