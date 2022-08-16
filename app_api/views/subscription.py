from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Subscription
from app_api.models import RareUser

import datetime

class SubscriptionView(ViewSet):
    """Level up game types view"""

    # def retrieve(self, request, pk):
    #     """Handle GET requests for single game type
    #     Returns:
    #         Response -- JSON serialized game type"""
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         serializer = PostSerializer(post)
    #         return Response(serializer.data)
    #     except Post.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        

    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        subs = Subscription.objects.all()
        author = request.query_params.get('author', None)
        if author is not None:
            follower=RareUser.objects.get(user=request.auth.user)
            subs = Subscription.objects.filter(author=author, follower=follower)
        serializer = SubscriptionSerializer(subs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations"""
        follower = RareUser.objects.get(user=request.auth.user)
        author = RareUser.objects.get(pk=request.data["author"])
        subscription = Subscription.objects.create(
            follower=follower,
            author=author,
            created_on= datetime.date.today(),
            ended_on=None
        )
        
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """handle put"""
        sub = Subscription.objects.get(pk=pk)
        sub.ended_on = datetime.date.today()
        sub.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        sub = Subscription.objects.get(pk=pk)
        sub.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Subscription
        fields = ('id', 'follower', 'author', 'created_on', 'ended_on')
        

