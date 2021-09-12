from blog.models import Comment, Post, Category, Profile, Tag, Account
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'published_at']
    prepopulated_fields = {"slug":("title",)}
    list_filter = ['categories', 'tags', 'status']
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Profile)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
admin.site.register(Comment, CommentAdmin)
class AccountAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active']
    list_display_links = ['email','first_name', 'last_name']
    readonly_fields = ['last_login', 'date_joined']
    ordering = ['-date_joined',]
    filter_horizontal = []
    list_filter = []
    fieldsets  = [] #will make the password read only

admin.site.register(Account, AccountAdmin)