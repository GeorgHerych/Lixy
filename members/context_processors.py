from django.urls import reverse


def user_dialogs(request):
    """Provide a lightweight list of potential dialogs for the authenticated user."""
    dialogs = []

    user = getattr(request, "user", None)

    if user and user.is_authenticated:
        followings = (
            user.followings.select_related("city", "country")
            .order_by("first_name", "last_name", "username")
        )
        follower_ids = set(user.followers.values_list("id", flat=True))

        for companion in followings:
            is_mutual = companion.id in follower_ids
            full_name = companion.get_full_name() or companion.username
            avatar_url = getattr(companion.avatar, "url", "") or "/media/avatars/default/default_avatar_light.png"

            dialogs.append(
                {
                    "username": companion.username,
                    "name": full_name,
                    "avatar": avatar_url,
                    "preview": (
                        "Взаємна симпатія — напишіть повідомлення!"
                        if is_mutual
                        else "Напишіть першими, щоб розпочати діалог."
                    ),
                    "url": reverse("dialog_detail", args=[companion.username]),
                    "is_mutual": is_mutual,
                }
            )

    return {"user_dialogs": dialogs}
