"""View module for handling requests about authors"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Author


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
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for authors
    """
    class Meta:
        model = Author
        fields = ('id', 'user', 'bio', 'profile_image_url')
