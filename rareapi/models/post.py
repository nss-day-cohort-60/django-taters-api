from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, related_name='post_category', null=True)
    title = models.CharField(max_length=155)
    publication_date = models.DateField(auto_now=False, auto_now_add=True)
    image_url = models.CharField(max_length=250)
    content = models.CharField(max_length=500)
    approved = models.BooleanField(default=False)
    reactions = models.ManyToManyField("Reaction", through="postreaction", related_name='reactions_of_post')
    tags = models.ManyToManyField("Tag", through="posttag", related_name='tags_of_post')

    @property
    def writer(self):
        return self.__writer

    @writer.setter
    def writer(self, value):
        self.__writer = value