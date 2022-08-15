from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from app_api.models import Reaction

class ReactionView(ViewSet):
    """ Rare reaction view
    """
    def list(self, request):
        """The GET for all reactions in the database

        Returns: 
            Response: JSON serialized list of tags
        """
        reactions = Reaction.objects.all()

        serializer = ReactionSerializer(reactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReactionSerializer(serializers.ModelSerializer):
    """
    JSON serializer for the tag data received
    """

    class Meta:
        model = Reaction
        fields = ('id', 'label')
