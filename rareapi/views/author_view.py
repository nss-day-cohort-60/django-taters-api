"""View module for handling requests about authors"""
from django.http import HttpResponseServerError
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Author, Subscription
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q


class AuthorView(ViewSet):
    """Level up authors view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single author

        Returns:
            Response -- JSON serialized author
        """
        user = Author.objects.get(user=request.auth.user)
        subscriptions = Subscription.objects.all()
        subscriptions = subscriptions.filter(subscriber_id=user)

        try: 
            author = Author.objects.get(pk=pk)
            subscriptions = subscriptions.filter(author_id=author)
            if subscriptions:
                author.subscribed = True
            else:
                author.subscribed = False

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
        authors = Author.objects.annotate(
            followers_count=Count('subscribers')
        )

        for author in authors:
            subscriptions = Subscription.objects.filter(Q(subscriber__user=request.auth.user) & Q(author_id=author))
            if subscriptions:
                author.subscribed = True
            else:
                author.subscribed = False

        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True)
    def subscribe(self, request, pk):
        """Post request for a user to sign up for an event"""

        current_user = Author.objects.get(user=request.auth.user)
        author = Author.objects.get(pk=request.data)
        author.subscribers.add(current_user)
        return Response({'message': 'Subscriber added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unsubscribe(self, request, pk):
        """Delete request for a user to leave an event"""

        current_user = Author.objects.get(user=request.auth.user)
        author = Author.objects.get(pk=pk)
        author.subscribers.remove(current_user)
        return Response({'message': 'Subscriber removed'}, status=status.HTTP_204_NO_CONTENT)

class SubscriberSerializer(serializers.ModelSerializer):
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
    followers_count = serializers.IntegerField(default=None)
    subscriber = SubscriberSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'user', 'bio', 'profile_image_url', 'subscriber', 'subscribed', 'full_name', 'followers_count')
