from datetime import datetime
from xmlrpc.client import DateTime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.comment import Comment
from app_api.models.post import Post
from ..models.rare_user import RareUser
import datetime



class CommentView(ViewSet):
    
    def retrieve(self, request, pk):
        """Handle Get requests for single comment
        Returns: JSON serialized comment"""
        
        try:
            
            comment = Comment.objects.get(pk=pk)
        
            Serializer = CommentSerializer(comment)
            return Response(Serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(sef, request):
        """Handle GET requests for all comments

        Return
            JSON serialized list of comments
        """
        
        comments = Comment.objects.all()
        
        post_id =request.query_params.get('post_id', None)
        if post_id is not None:
                comments = comments.filter(post_id=post_id)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST Requests

        Return ---JSON comment instance
        """
        
        post = Post.objects.get(pk=request.data["post_id"])
        author = RareUser.objects.get(user_id=request.auth.user)
        
        comment = Comment.objects.create(
        
        post = post,
        author = author,    
        content = request.data["content"],
        created_on = datetime.date.today()
        )
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a comment
        
        Response -- Empty body with 204 status code"""
        
        comment = Comment.objects.get(pk=pk)
        
        post = Post.objects.get(pk=request.data["post"])
        comment.post = post
        
        author = RareUser.objects.get(pk=request.data["user_id"])
        comment.author = author
        
        comment.created_on = request.data["created_on"]
        
        comment.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT) 
    
    def destroy(self, request, pk):
    
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)     
        
        
class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    
    class Meta:
        model = Comment
        fields = ( 'id', 'post_id', 'author_id', 'content', 'created_on' )
        depth = 2       
