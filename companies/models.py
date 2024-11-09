from django.db import models

# Create your models here.
from core.models import Timestamped


class Company(Timestamped):
    name = models.CharField(max_length=255)
    profiles = models.ManyToManyField("profiles.Profile")


    class Meta:
        default_related_name = 'companies'
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name