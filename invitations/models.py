from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Invitation(models.Model):
    email = models.CharField(max_length=255)
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'invitations'
        verbose_name = 'invitation'
        verbose_name_plural = 'invitations'
        unique_together = (('user', 'email', 'company'),)
        indexes = [
            models.Index(fields=['user', 'email', 'company']),
        ]

    def __str__(self):
        return f"{self.email}"