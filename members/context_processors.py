from members.services.dialogs import collect_user_dialogs


def user_dialogs(request):
    """Provide a lightweight list of potential dialogs for the authenticated user."""

    user = getattr(request, "user", None)

    if not user:
        return {"user_dialogs": []}

    return {"user_dialogs": collect_user_dialogs(user)}
