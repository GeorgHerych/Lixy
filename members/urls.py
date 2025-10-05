from django.urls import path
from members import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('discover/', views.discover, name='discover'),
    path('profile/<str:username>/settings/notifications/', views.profile_settings_notifications, name='profile_settings_notifications'),
    path('profile/<str:username>/settings/privacy/', views.profile_settings_privacy, name='profile_settings_privacy'),
    path('profile/<str:username>/settings/rules/', views.profile_settings_rules, name='profile_settings_rules'),
    path('profile/<str:username>/settings/subscriptions/', views.profile_settings_subscriptions, name='profile_settings_subscriptions'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/edit-profile/<str:username>', views.edit_profile, name='edit_profile'),
    path('profile/delete-banner/', views.delete_banner, name='delete_banner'),
    path('profile/delete-avatar/', views.delete_avatar, name='delete_avatar'),
    path('dialogs/', views.dialog_list, name='dialog_list'),
    path('dialogs/<str:username>/', views.dialog_detail, name='dialog_detail'),
    path('edit-profile/get-cities/', views.get_cities, name='get_cities'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),
    path('remove/<str:username>', views.remove, name='remove'),
    path('followings/<str:username>', views.followings, name='followings'),
    path('followers/<str:username>', views.followers, name='followers'),
]