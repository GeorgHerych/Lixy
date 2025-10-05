from __future__ import annotations

from datetime import timedelta
from typing import Dict, List

from django.urls import reverse
from django.utils import timezone

from members.models import Member


DIALOG_PREVIEW_MUTUAL = "Взаємна симпатія — напишіть повідомлення!"
DIALOG_PREVIEW_FIRST_MESSAGE = "Напишіть першими, щоб розпочати діалог."


def _get_avatar_url(member: Member) -> str:
    avatar_url = getattr(member.avatar, "url", "")
    if avatar_url:
        return avatar_url
    return "/media/avatars/default/default_avatar_light.png"


def _build_preview(is_mutual: bool) -> str:
    if is_mutual:
        return DIALOG_PREVIEW_MUTUAL
    return DIALOG_PREVIEW_FIRST_MESSAGE


def _shorten_preview(text: str, length: int = 80) -> str:
    if len(text) <= length:
        return text
    return f"{text[: length - 1]}…"


def collect_user_dialogs(user: Member) -> List[Dict[str, object]]:
    dialogs: List[Dict[str, object]] = []

    if not user.is_authenticated:
        return dialogs

    follower_ids = set(user.followers.values_list("id", flat=True))
    followings = user.followings.select_related("city", "country").order_by(
        "first_name", "last_name", "username"
    )
    now = timezone.now()
    online_threshold = timedelta(minutes=5)

    for companion in followings:
        is_mutual = companion.id in follower_ids
        preview = _build_preview(is_mutual)
        last_login = companion.last_login
        is_online = bool(last_login and now - last_login <= online_threshold)
        full_name = companion.get_full_name() or companion.username

        dialogs.append(
            {
                "username": companion.username,
                "name": full_name,
                "avatar": _get_avatar_url(companion),
                "preview": preview,
                "preview_short": _shorten_preview(preview),
                "url": reverse("dialog_detail", args=[companion.username]),
                "is_mutual": is_mutual,
                "is_online": is_online,
            }
        )

    return dialogs
