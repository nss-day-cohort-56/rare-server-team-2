import base64
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
import uuid


from django.core.files.base import ContentFile



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
        """Response -- Empty body with 204 status code"""
        user = User.objects.get(pk=pk)
        rare_user = RareUser.objects.get(user=request.auth.user)
        user.is_staff = not user.is_staff
        # Create a new instance of the game picture model you defined
        # Example: game_picture = GamePicture()
        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["id"]}-{uuid.uuid4()}.{ext}')

        # Give the image property of your game picture instance a value
        # For example, if you named your property `action_pic`, then
        # you would specify the following code:
        #
        #       game_picture.action_pic = data

        # Save the data to the database with the save() method
        rare_user.profile_image_url = data
        rare_user.save()
        user.save()
        serializer = UserSerializer(user)
        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data, status=status.HTTP_200_OK) 
        
    @action(methods=['put'], detail=True)
    def change_active_status(self, request, pk):
        """Handle PUT requests for a user
        
        Response --  200 OK status code"""
        
        user = User.objects.get(pk=pk)
        user.is_active = not user.is_active
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK) 


    @action(methods=["put"], detail=True)
    def change_staff_status(self, request, pk):
        user = User.objects.get(pk=pk)
        user.is_staff = not user.is_staff
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
        # ordering =  ['username']

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers"""
    user = UserSerializer()
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'created_on')