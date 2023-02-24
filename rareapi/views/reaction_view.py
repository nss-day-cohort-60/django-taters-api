"""View module for handling requests about reactions"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Reaction
from django.db.models import Count
from django.db.models import Q




class ReactionView(ViewSet):

    def list(self, request):
        """Handle GET requests to get all reactions
        Returns:
            Response -- JSON serialized list of reactions
        """


        if "post" in request.query_params:
            postId = self.request.query_params.get('post')
            reactions = Reaction.objects.all()

            reactions = reactions.annotate(
                post_reaction_count=Count('reactions_of_post', filter=Q(reactions_of_post=postId))
            )
            # for reaction in reactions:
            #     post_reaction_count = reactions.annotate(Count('reactions_of_post', filter=Q(pk=postId)))
                
        else:
            reactions = Reaction.objects.all()

        serializer = ReactionSerializer(reactions, many=True)

        # reactions = Reaction.objects.annotate(attendees_count=Count('reactions_of_post'))

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""

    post_reaction_count = serializers.IntegerField(default=None)

    class Meta:
        model = Reaction
        fields = ('id', 'label', 'emoji_icon', 'post_reaction_count')
