from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.contrib.auth.models import User


from app_api.models.rare_user import RareUser

class RareUserView(ViewSet):
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
        rare_users = RareUser.objects.all().order_by("user__username")

        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a user
        
        Response -- Empty body with 204 status code"""
        

        user = User.objects.get(pk=pk)
        user.is_staff = not user.is_staff
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')
        # ordering =  ['username']

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers"""
    user = UserSerializer()
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'created_on', 'active')
