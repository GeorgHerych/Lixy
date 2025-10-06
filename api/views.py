from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from members.models import Member
from posts.models import HiddenPost, Post, SavedPost

from .serializers import (
    AuthTokenSerializer,
    HiddenPostSerializer,
    MemberSummarySerializer,
    PostSerializer,
    SavedPostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = (
            Post.objects.select_related("member", "member__country", "member__city")
            .prefetch_related("attachments")
            .order_by("-pub_date")
        )
        member: Member = self.request.user
        if member.is_authenticated:
            hidden_post_ids = HiddenPost.objects.filter(member=member).values_list(
                "post_id", flat=True
            )
            queryset = queryset.exclude(id__in=hidden_post_ids)
        return queryset

    def perform_create(self, serializer):
        serializer.save(member=self.request.user, pub_date=timezone.now())

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def save(self, request, pk=None):
        post = self.get_object()
        SavedPost.objects.get_or_create(member=request.user, post=post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def unsave(self, request, pk=None):
        post = self.get_object()
        SavedPost.objects.filter(member=request.user, post=post).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def hide(self, request, pk=None):
        post = self.get_object()
        HiddenPost.objects.get_or_create(member=request.user, post=post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def unhide(self, request, pk=None):
        post = self.get_object()
        HiddenPost.objects.filter(member=request.user, post=post).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SavedPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SavedPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            SavedPost.objects.filter(member=self.request.user)
            .select_related("post", "post__member")
            .prefetch_related("post__attachments")
        )


class HiddenPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HiddenPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            HiddenPost.objects.filter(member=self.request.user)
            .select_related("post", "post__member")
            .prefetch_related("post__attachments")
        )


class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MemberSummarySerializer
    queryset = Member.objects.prefetch_related("followers", "followings").order_by("username")


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def obtain_auth_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})
