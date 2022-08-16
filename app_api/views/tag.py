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
        """The GET for all tags in the database, in alphabetical order

        Returns:
            Response: JSON serialized list of tags
        """
        tags = Tag.objects.all().order_by("label")

        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """The GET for on tag in the database

        Returns:
            response: JSON serializer game gor the selected key
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """ POST operation for a new tag

        Returns:
            Response: JSON serialized tag instance
        """

        tag = Tag.objects.create(
            label=request.data["label"]
        )

        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """ PUT request for the selected tag

        Returns:
            Response: Empty body with a 204 status code.
        """

        tag=Tag.objects.get(pk=pk)
        tag.label=request.data["label"]
        tag.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """ THE DELETE request for a tag
        """
        tag = Tag.objects.get(pk=pk)

        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """
    JSON serializer for the tag data received
    """

    class Meta:
        model = Tag
        fields = ('id', 'label')
