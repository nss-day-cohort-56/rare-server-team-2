from django.db import models

class Reaction(models.Model):
    label = models.CharField(max_length=30)
    image_url = models.CharField(max_length=200)
