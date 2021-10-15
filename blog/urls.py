from django.urls import path
from . import views
from .views import PasswordsChangeView, all_articles, categories
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/category/<id>/', views.single_category, name='single_category'),
    path('blog/<slug>/', views.post_detail, name='post-detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/posts/all-posts/', views.show_post, name='show-post'),
    path('dashboard/posts/add-post/', views.add_post, name='add-post'),
    path('dashboard/posts/update-post/<slug>/', views.update_post, name='update-post'),
    path('dashboard/posts/delete-post/<slug>/', views.delete_post, name='delete-post'),
    path('dashboard/categories/', views.categories, name='categories'),
    path('dashboard/categories/<id>/', views.update_categories, name='update-categories'),
    path('dashboard/categories/delete/<id>/', views.delete_categories, name='delete-categories'),
    path('dashboard/comments/', views.all_comments, name='comments'),
    path('dashboard/comments/<id>/', views.update_comments, name='update-comments'),
    path('dashboard/comments/delete/<id>/', views.delete_comments, name='delete-comments'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('dashboard/biography/', views.biography, name='biography'),
    path('dashboard/biography/update/<id>/', views.biography_update, name='biography-update'),
    # path('register/', views.register, name='register'),
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
