from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Post
from app_api.models import RareUser
from app_api.models import Category
from app_api.models import PostTag
from app_api.models import Tag
from django.db.models import Q
import datetime

class PostView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type"""
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        

    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        posts = Post.objects.all()
        search_text = self.request.query_params.get('q', None)
        if search_text is not None:
            posts = Post.objects.filter(
                    Q(title__contains=search_text) |
                    Q(content__contains=search_text))
        user = request.query_params.get('user', None)
        if user is not None:
            posts = Post.objects.filter(user=user)
        category = request.query_params.get('category', None)
        if category is not None:
            posts = Post.objects.filter(category=category)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations"""
        user = RareUser.objects.get(user=request.auth.user)
        cat = Category.objects.get(pk=request.data["category_id"])
        post = Post.objects.create(
            title=request.data["title"],
            user=user,
            category=cat,
            publication_date= datetime.date.today(),
            image_url=request.data["image_url"],
            content=request.data["content"],
            approved=True
        )
        post.tags.add(*request.data['tags'])
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """handle put"""
        post = Post.objects.get(pk=pk)
        cat = Category.objects.get(pk=request.data["category_id"])
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.category = cat
        post.content = request.data["content"]
        post.save()
        post.tags.clear()
        post.tags.add(*request.data['tags'])
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url',  'content', 'tags', 'reactions', 'approved')
        depth = 2
