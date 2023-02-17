from django.db import models

class PostReaction(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='user_reaction')
    reaction = models.ForeignKey("Reaction", on_delete=models.SET_NULL, related_name='post_reaction')