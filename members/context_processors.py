from members.services.dialogs import collect_user_dialogs


def user_dialogs(request):
    """Provide a lightweight list of potential dialogs for the authenticated user."""

    user = getattr(request, "user", None)

    if not user:
        return {"user_dialogs": [], "user_unread_dialogs_count": 0}

    dialogs = collect_user_dialogs(user)
    unread_dialogs_count = sum(1 for dialog in dialogs if dialog.get("unread_count"))

    return {
        "user_dialogs": dialogs,
        "user_unread_dialogs_count": unread_dialogs_count,
    }
