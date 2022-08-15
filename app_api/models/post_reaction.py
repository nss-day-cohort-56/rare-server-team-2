from django.db import models

class PostReaction(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_id_reaction")
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE, related_name="reaction_id")
