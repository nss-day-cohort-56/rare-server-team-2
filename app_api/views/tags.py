from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from app_api.models import Tag

class TagView(ViewSet):
    """ Rare tags view
    """
    def list(self, request):
        """The GET for all tags in the database

        Returns: 
            Response: JSON serialized list of tags
        """
        tags = Tag.objects.all.order_by("label")

        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagSerializer(serializers.ModelSerializer):
    """
    JSON serializer for the tag data received
    """

    class Meta:
        model = Tag
        fields = ('id', 'label')