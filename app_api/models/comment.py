from django.db import models

class Comment( models.model):
    
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_id")
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="author_id")
    content = models.TextField(max_length=200)
    created_on= models.DateField()