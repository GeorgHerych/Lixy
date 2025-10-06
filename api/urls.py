from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HiddenPostViewSet, MemberViewSet, PostViewSet, SavedPostViewSet, obtain_auth_token

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"saved-posts", SavedPostViewSet, basename="saved-post")
router.register(r"hidden-posts", HiddenPostViewSet, basename="hidden-post")
router.register(r"members", MemberViewSet, basename="member")

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api-token"),
    path("", include(router.urls)),
]
