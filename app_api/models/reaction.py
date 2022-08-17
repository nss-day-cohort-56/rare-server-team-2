from django.db import models

from app_api.models import PostReaction

class Reaction(models.Model):
    label = models.CharField(max_length=30)
    image_url = models.CharField(max_length=200)
    
    @property
    def reaction_count(self):
        return self.__reaction_count

    @reaction_count.setter
    def reaction_count(self, value):
        self.__reaction_count=len(PostReaction.objects.filter(post=value, reaction=self))
