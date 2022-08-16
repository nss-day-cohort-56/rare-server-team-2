from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.rare_user import RareUser

class RareUserView(ViewSet):
    """Rare user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single rare_user

        Returns:
            Response -- JSON serialized rare_user
        """
        try:
            rare_user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(rare_user)
            return Response(serializer.data)
        except rare_user.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all rare_user

        Returns:
            Response -- JSON serialized list of rare_user
        """
        rare_users = RareUser.objects.all()
        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data)

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for rare_user types
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'created_on', 'active')
        depth = 2