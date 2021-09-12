from django.db import models
from django.template.defaultfilters import truncatechars

# Create your models here.
class Biography(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/bio/", null=True)
    facebook = models.URLField(max_length=300, null=True, blank=True, default="#")
    instagram = models.URLField(max_length=300, null=True, blank=True)
    twitter = models.URLField(max_length=300, null=True, blank=True, default="#")
    youtube = models.URLField(max_length=300, null=True, blank=True, default="#")
    snapchat = models.URLField(max_length=300, null=True, blank=True, default="#")

    @property
    def short_bio(self):
        return truncatechars(self.bio, 80)

    class Meta:
        verbose_name = "biography"
        verbose_name_plural = "my biography"
        
    def __str__(sellf):
        return sellf.name
