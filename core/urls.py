"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler500, url
from django.conf import settings
from django.views.static import serve

from django.conf.urls import handler404
from django.contrib import admin, sitemaps
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    "posts":PostSitemap,
}

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('marketing/', include('marketing.urls')),
    path('froala_editor/', include('froala_editor.urls')),
    url('avatar/', include('avatar.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
						name='django.contrib.sitemaps.views.sitemap')

] 
# urlpatterns += static(settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


# urlpatterns += staticfiles_urlpatterns()

handler404 = "helpers.views.page_not_found"
handler500 = "helpers.views.page_server_error"
