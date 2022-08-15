from django.db import models

class PostReaction( models.model):
    
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_id")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_id")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="reaction_id")