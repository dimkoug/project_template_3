from django.db import models

# Create your models here.
from core.models import Timestamped


class Company(Timestamped):
    name = models.CharField(max_length=255)
    profiles = models.ManyToManyField("profiles.Profile", through="CompanyProfile")


    class Meta:
        default_related_name = 'companies'
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name
    

class CompanyProfile(Timestamped):
    company = models.ForeignKey("Company",on_delete=models.CASCADE)
    profile = models.ForeignKey("profiles.Profile",on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


    class Meta:
        default_related_name = 'company_profiles'
        indexes = [
            models.Index(fields=['company', 'profile']),  # Composite index
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'profile'], name='%(app_label)s_%(class)s_unique_company_profile')
        ]



