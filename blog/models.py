from django.db import models
from django.urls import reverse
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import default, slugify
from froala_editor.fields import FroalaField
from PIL import Image
from taggit.managers import TaggableManager
from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER
from marketing.models import SignUp

# Create your models here.

class MyAccountManager(BaseUserManager):
    #creating a normal user 
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    #creating a superuser
    def create_superuser (self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username= username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True 
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    #required, these are mandatory when creating a custom user model
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    # REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.first_name+ ' ' +self.last_name

    #must be added when creating a custom user model
    def has_perm(self, perm, obj=None):
        return self.is_admin #basically if he person is an admin he has a the permission

    def has_module_perms(self, add_label):
        return True #this should always return true

# Signal to make user is_active on registration
@receiver(post_save, sender=Account)
def default_to_non_active(sender, instance, created, **kwargs):
    if created:
        instance.is_active = True
        instance.save()


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="profile", null=True)
    image = models.ImageField(default='default.png', upload_to='images/profile_images/', null=True, blank=True)

    def __str__(self):
        name = self.user.first_name+ ' '+self.user.last_name
        return f'{name} profile'

class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        name = self.category_name
        return f'{name} category'
    # def __str__(self):
    #     return 'Category {} by'.format(self.category_name)

class Tag(models.Model):
    tag_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.tag_name

class Post(models.Model):
    STATUS = (
        ('published', 'PUBLISHED'),
        ('draft', 'DRAFT')
    )
    title = models.CharField(max_length=1000, null=True)
    slug = models.SlugField(max_length=1000 ,null=True, unique=True)
    author = models.ForeignKey(Account, on_delete=CASCADE, null=True)
    # description = models.TextField(null=True, blank=True)
    content = models.TextField()
    # content = FroalaField()
    blog_image = models.ImageField(upload_to='images/blog/', null=True, default='blog_default.png')
    categories = models.ForeignKey(Category, null=True, on_delete=CASCADE, blank=True)
    blog_video = models.FileField(blank=True, upload_to='videos/blog/', null=True, verbose_name='upload a video')
    # comments = models.ManyToManyField(Comment, blank=True)
    # comment_count = models.IntegerField(default=0, null=True)
    tag = TaggableManager()
    status = models.CharField(max_length=50, null=True, choices=STATUS, default='published')
    featured = models.BooleanField(default=False)
    post_views = models.IntegerField(default=0, null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return self.title    
# @receiver(post_save, sender=Post)
# def SendEmail(sender , instance, created, **kwargs):
#     if created:
#         emails = list(SignUp.objects.values('email'))
#         recepients = []
#         for i in range(0, len(emails)):
#             recepients.append(emails[i]['email'])
#             pass
#         send_mail('New Post on BlesiDiary','hello blesidiary welcome you once again to view our content'+' '+str(instance.title), EMAIL_HOST_USER, recepients, fail_silently=False)
#         pass
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    content = models.TextField(null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.name)
    # def __unicode__(self):
    #     return self.name