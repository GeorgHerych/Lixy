from django.urls import path
from members import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/edit-profile/<str:username>', views.edit_profile, name='edit_profile'),
    path('profile/delete-banner/', views.delete_banner, name='delete_banner'),
    path('profile/delete-avatar/', views.delete_avatar, name='delete_avatar'),
    path('edit-profile/get-cities/', views.get_cities, name='get_cities'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),
    path('remove/<str:username>', views.remove, name='remove'),
    path('followings/<str:username>', views.followings, name='followings'),
    path('followers/<str:username>', views.followers, name='followers'),
]