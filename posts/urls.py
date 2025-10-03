from django.urls import path
from posts import views

urlpatterns = [
    path('', views.posts, name='posts'),
    path('following/', views.following_posts, name='following_posts'),
    path('posts/delete-post/<int:post_id>', views.delete_post, name='delete_post'),
    path('posts/edit-post/<int:post_id>', views.edit_post, name='edit_post'),
    path('posts/hide-post/<int:post_id>', views.hide_post, name='hide_post'),
    path('posts/saved-posts/', views.saved_posts, name='saved_posts'),
    path('posts/save-post/<int:post_id>', views.save_post, name='save_post'),
    path('posts/unsave-post/<int:post_id>', views.unsave_post, name='unsave_post'),
    path('posts/<int:post_id>/delete-attachment/<int:attachment_id>', views.delete_attachment, name='delete_attachment'),
]