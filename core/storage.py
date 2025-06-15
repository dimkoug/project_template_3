try:
    from django.core.files.storage import FileSystemStorage, get_storage_class
except ImportError:
    from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

#class OverwriteStorage(get_storage_class()):

#    def _save(self, name, content):
#        self.delete(name)
#        return super(OverwriteStorage, self)._save(name, content)
#
#    def get_available_name(self, name, max_length):
#        return name

class OverwriteStorage(FileSystemStorage):
    """
    A storage backend that *always* overwrites files
    with the same name instead of creating «foo_1.txt», «foo_2.txt», …
    """

    # Django ≥ 5.1 added the `allow_overwrite` kwarg –  
    # use it instead of overriding _save()/get_available_name().
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("allow_overwrite", True)
        super().__init__(*args, **kwargs)
