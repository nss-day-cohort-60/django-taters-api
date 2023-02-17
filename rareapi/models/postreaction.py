from django.db import models

class PostReaction(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='posts')
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name='post_tags')
    reaction = models.ForeignKey("Reaction", on_delete=models.SET_NULL, related_name='post_reaction')