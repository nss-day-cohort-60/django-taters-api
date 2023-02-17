from django.db import models

class Reaction(models.Model):
    emoji = models.CharField(max_length=50)