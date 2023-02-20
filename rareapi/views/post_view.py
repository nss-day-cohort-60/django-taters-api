"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Reaction, Tag


class PostView(ViewSet):
    """Rare post view"""

    def retrieve(self, request, pk):
        """Handle GET requests for events

        Returns:
            Response -- JSON serialized events
        """
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        # reactions = Reaction.objects.all()
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'emoji_url')


class PostTagSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Tag
        fields = ('id', 'label',)


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """

    reactions = PostReactionSerializer(many=True)
    tags = PostTagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'category',
                  'title', 'publication_date', 'image_url', 'content', 'approved',
                  'reactions', 'tags')
