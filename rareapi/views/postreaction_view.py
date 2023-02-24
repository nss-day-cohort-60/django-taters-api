"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import PostReaction, Author, Post, Reaction


class PostReactionView(ViewSet):
    """Rare post view"""

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        try:
            author = Author.objects.get(user=request.auth.user)
        except Author.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = Post.objects.get(pk=request.data['post'])
        except Post.DoesNotExist:
            return Response({'message': 'You sent an invalid post Id'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            reaction = Reaction.objects.get(pk=request.data['reaction'])
        except Post.DoesNotExist:
            return Response({'message': 'You sent an invalid reaction Id'}, status=status.HTTP_404_NOT_FOUND)

        postreaction = PostReaction.objects.create(
            post=post,
            author=author,
            reaction=reaction
        )

        serializer = PostReactionSerializer(postreaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PostReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""

    class Meta:
        model = PostReaction
        fields = ('id','post', 'author', 'reaction')