"""View module for handling requests about authors"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Author
from rest_framework.decorators import action
from django.contrib.auth.models import User


class AuthorView(ViewSet):
    """Level up authors view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single author

        Returns:
            Response -- JSON serialized author
        """

        try: 
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist: 
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        serialized = AuthorSerializer(author, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all authors

        Returns:
            Response -- JSON serialized list of authors
        """
        authors = Author.objects.all()
        follower = Author.objects.get(user=request.auth.user)

        # Set the `joined` property on every event
        for author in authors:
            # Check to see if the gamer is in the attendees list on the event
            author.subscribed = follower in author.followers.all()

        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        follower = Author.objects.get(user=request.auth.user)
        author = Author.objects.get(pk=pk)
        author.followers.add(follower)
        return Response({'message': 'Subscriber added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        follower = Author.objects.get(user=request.auth.user)
        author = Author.objects.get(pk=pk)
        author.followers.remove(follower)
        return Response({'message': 'Subscriber removed'}, status=status.HTTP_204_NO_CONTENT)

class FollowerSerializer(serializers.ModelSerializer):
    """JSON serializer for attendees
    """
    class Meta:
        model = Author
        fields = ('id', 'full_name')

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for authors
    """
    user = UserSerializer(many=False)


    follower_of_author = FollowerSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'user', 'bio', 'profile_image_url', 'follower_of_author', 'subscribed', 'full_name', )
