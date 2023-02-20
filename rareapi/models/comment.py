from django.db import models

class Comment(models.Model):

    author = models.ForeignKey("Author", null=True, blank=True, on_delete=models.CASCADE, related_name='author_comment')
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='post_comment')
    content = models.CharField(max_length=300)