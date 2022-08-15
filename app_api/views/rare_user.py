from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action

from app_api.models.rare_user import RareUser

class UserView(ViewSet):
    """Rare User view"""

    def retrieve(self, request, pk):
        """handle GET requests for a single user
        """

        try:
            user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(user)
            return Response(serializer.data)
        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all RareUsers

        Returns:
            Response -- JSON serialized list of RareUsers
        """
        rare_users = RareUser.objects.all()

        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data)

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers"""
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'created_on', 'active')
