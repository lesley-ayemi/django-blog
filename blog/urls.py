from django.urls import path
from . import views
from .views import PasswordsChangeView, all_articles
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<slug>/', views.post_detail, name='post-detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/posts/all-posts/', views.show_post, name='show-post'),
    path('dashboard/posts/add-post/', views.add_post, name='add-post'),
    path('dashboard/posts/update-post/<slug>/', views.update_post, name='update-post'),
    path('dashboard/posts/delete-post/<slug>/', views.delete_post, name='delete-post'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('articles/', views.all_articles, name='all-articles'),
    path('articles/search/', views.search_article, name='search_article'),

    path('dashboard/password/', PasswordsChangeView.as_view(template_name='dashboard/profile/change-password.html'), name='password'),
    # path('password', auth_views.PasswordChangeView.as_view(template_name='dashboard/profile/change-password.html')),
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
]
