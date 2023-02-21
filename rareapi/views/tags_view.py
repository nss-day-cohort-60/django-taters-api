"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Tag


class TagView(ViewSet):
    """Rare tags view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single tag
        Returns:
            Response -- JSON serialized tag
        """
        try:

            tag = Tag.objects.get(pk=pk) #make connection with server to return single query set where the primary key matches the pk requested by the client and assigns the object instance found to the tag variable
        
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TagSerializer(tag) #passes the instance stored in tag through serializer to become a JSON stringified object and assigns it to serializer variable

        return Response(serializer.data, status=status.HTTP_200_OK) # returns serializer data to the client as a response. Response body is JSON stringified object of requested data.


    def list(self, request):
        """Handle GET requests to get all tags
        Returns:
            Response -- JSON serialized list of tags
        """
        # Make connection with server to retrieve a query set of all tags items requested by client and assign the found instances to the tags variable
        tags = Tag.objects.all()
        #passes instances stored in tags variable to the serializer class to construct data into JSON stringified objects, which it then assigns to variable serializer
        serializer = TagSerializer(tags, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK) #Constructs response and returns data requested by the client in the response body as an array of JSON stringified objects
        
    def create(self, request):
            """Handle POST operations
            Returns
                Response -- JSON serialized tag instance
            """

            tag = Tag.objects.create(
                label=request.data["label"]
            )
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a tag
        Returns:
            Response -- Empty body with 204 status code
        """

        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    # Converts meta data requested to JSON stringified object using Tag as model
    class Meta: # configuration for serializer
        model = Tag # model to use
        fields = ('id', 'label') # fields to include