from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100)
    language = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.theme} - {self.language} for user id {self.user}"

    class Meta:
        db_table = 'settings'
