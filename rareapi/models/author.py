from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url = models.CharField(max_length=100)


    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'