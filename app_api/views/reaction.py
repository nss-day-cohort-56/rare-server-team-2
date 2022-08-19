from urllib import response
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
    
    
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized category instance
        """
        reaction = Reaction.objects.create(
        label = request.data['label'],
        image_url = request.data['image_url']
            )

        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """ PUT request for the selected reaction

        Returns:
            Response: Empty body with a 204 status code.
        """

        reaction=Reaction.objects.get(pk=pk)
        reaction.label=request.data["label"]
        reaction.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    
    def destroy(self, request, pk):
        reaction = Reaction.objects.get(pk=pk)
        reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    
    

class ReactionSerializer(serializers.ModelSerializer):
    """
    JSON serializer for the tag data received
    """

    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
