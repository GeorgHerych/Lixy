from django.contrib.auth import authenticate
from rest_framework import serializers

from members.models import Member
from posts.models import HiddenPost, Post, PostAttachment, SavedPost


class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = PostAttachment
        fields = ["id", "type", "attachment", "url"]

    def get_url(self, attachment: PostAttachment) -> str:
        request = self.context.get("request")
        if request is not None and attachment.attachment:
            return request.build_absolute_uri(attachment.attachment.url)
        if attachment.attachment:
            return attachment.attachment.url
        return ""


class MemberSummarySerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar_url",
            "bio",
            "country",
            "city",
        ]
        depth = 1

    def get_avatar_url(self, member: Member) -> str | None:
        request = self.context.get("request")
        if member.avatar and hasattr(member.avatar, "url"):
            if request is not None:
                return request.build_absolute_uri(member.avatar.url)
            return member.avatar.url
        return None


class PostSerializer(serializers.ModelSerializer):
    member = MemberSummarySerializer(read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    is_saved = serializers.SerializerMethodField()
    is_hidden = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "pub_date",
            "member",
            "attachments",
            "is_saved",
            "is_hidden",
        ]

    def get_is_saved(self, post: Post) -> bool:
        member: Member | None = self._get_request_user()
        if member and member.is_authenticated:
            return SavedPost.objects.filter(member=member, post=post).exists()
        return False

    def get_is_hidden(self, post: Post) -> bool:
        member: Member | None = self._get_request_user()
        if member and member.is_authenticated:
            return HiddenPost.objects.filter(member=member, post=post).exists()
        return False

    def _get_request_user(self) -> Member | None:
        request = self.context.get("request")
        if request:
            return request.user
        return None


class SavedPostSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = SavedPost
        fields = ["id", "post", "saved_at"]


class HiddenPostSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = HiddenPost
        fields = ["id", "post", "saved_at"]


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                attrs["user"] = user
                return attrs
        msg = "Unable to log in with provided credentials."
        raise serializers.ValidationError(msg, code="authorization")
