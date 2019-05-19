from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.PositiveIntegerField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_number = models.PositiveIntegerField(null=True, blank=True)
    code_melli = models.PositiveIntegerField(null=True, blank=True)
    bank_account = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

