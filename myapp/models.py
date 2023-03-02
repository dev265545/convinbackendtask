from django.db import models
from django.contrib.auth.models import User

class GoogleCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=200, null=True, blank=True)
    refresh_token = models.CharField(max_length=200, null=True, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username