from django.db import models

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_id")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="author_id_comment")
    content = models.TextField(max_length=200)
    created_on= models.DateField()
