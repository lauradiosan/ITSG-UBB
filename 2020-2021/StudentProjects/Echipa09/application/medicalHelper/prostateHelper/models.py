from django.db import models


# Create your models here.

class Image(models.Model):
    original = models.ImageField(upload_to='images/')
