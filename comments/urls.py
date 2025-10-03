from django.urls import path
from comments import views

urlpatterns = [
    path('<int:post_id>/comments/', views.comments, name='comments'),
    path('<int:post_id>/comments/edit-comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('<int:post_id>/comments/delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]