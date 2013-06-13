from django.db import models

# Create your models here.

class Setting(models.Model):
    setting = models.CharField(max_length=200)
    value = models.CharField(max_length=255)

class DashboardURLs(models.Model):
    url = models.TextField()
