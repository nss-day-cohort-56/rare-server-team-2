import base64
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from app_api.models import DemotionQueue
from app_api.models.rare_user import RareUser


class DemotionView(ViewSet):
    """Rare User view"""

    def list(self, request):
        """handle GET request WITH THE PK OF THE PENDING APPROVAL RAREUSER
        """
        try:
            user = self.request.query_params.get('user', None)
            if user is not None:
                demotion = DemotionQueue.objects.get(admin=user)
                serializer = DemotionSerializer(demotion)
                return Response(serializer.data)
        except DemotionQueue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """ POST operation for a new tag
        Returns:
            Response: JSON serialized tag instance
        """
        demote = DemotionQueue.objects.create(
            admin=RareUser.objects.get(user=request.data["admin"]),
            approver_one=RareUser.objects.get(user=request.auth.user),
            action=request.data['action']
        )
        serializer = DemotionSerializer(demote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        demote = DemotionQueue.objects.get(pk=pk)
        demote.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class DemotionSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers"""
    class Meta:
        model = DemotionQueue
        fields = ('id', 'admin', 'action', 'approver_one')
