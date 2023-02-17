from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='post_category')
    title = models.CharField(max_length=155)
    publication_date = models.DateField()
    image_url = models.ImageField(upload_to='images/')
    content = models.CharField(max_length=155)
    approved = models.BooleanField(default=False)
