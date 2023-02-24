from django.db import models

class Reaction(models.Model):
    label = models.CharField(max_length=25)
    emoji_icon = models.CharField(max_length=1)