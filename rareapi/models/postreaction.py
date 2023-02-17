from django.db import models
from django.contrib.auth.models import User

class PostReaction(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='post_reactions')
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name='user_reaction')
    reaction = models.ForeignKey("Reaction", on_delete=models.SET_NULL, related_name='post_reaction', null=True)