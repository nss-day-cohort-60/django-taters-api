from django.db import models

class Subscription(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='author_with_subscribers')
    subscriber = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='subscribed_follower')
    created_on = models.DateField(auto_now=False, auto_now_add=True)
