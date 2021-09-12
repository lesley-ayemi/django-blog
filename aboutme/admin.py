from django.contrib import admin
from .models import Biography
# Register your models here.
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'short_bio']
    # def bio(self, obj):
    #     return obj.bio[:10]
    # bio.short_description = "description"
admin.site.register(Biography, AboutMeAdmin)