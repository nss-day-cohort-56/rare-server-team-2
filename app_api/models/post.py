from django.db import models


class Post(models.Model):
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    publication_date = models.DateField()
    image_url = models.ImageField(
        upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)
    content = models.CharField(max_length=2000)
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="post_tags")
    reactions = models.ManyToManyField("Reaction", through="PostReaction", related_name="post_reaction")