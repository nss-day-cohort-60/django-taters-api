"""View module for handling requests about reactions"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Reaction


class ReactionView(ViewSet):

    def list(self, request):
        """Handle GET requests to get all reactions
        Returns:
            Response -- JSON serialized list of reactions
        """
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""

    class Meta:
        model = Reaction
        fields = ('id', 'label', 'emoji_url')
