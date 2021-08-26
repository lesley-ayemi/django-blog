from django.db import models
from django.urls import reverse
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.category_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.tag_name

class Post(models.Model):
    STATUS = (
        'published', 'PUBLISHED',
        'draft', 'DRAFT',
    )
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField()
    author = models.ForeignKey()
    body = models.TextField(null=True, blank=True)
    blog_image = models.ImageField(upload_to='images/blog/' ,null=True, blank=True)
    categories = models.ForeignKey(Category, null=True, on_delete=CASCADE, blank=True)
    tags = models.ManyToManyRel(related_name=Tag, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published']

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"sluf": self.slug})
    
    