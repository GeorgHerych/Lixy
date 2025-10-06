from __future__ import annotations

from typing import List

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone

from members.models import DialogMessage
from members.services.dialog_realtime import dialog_group_name

Member = get_user_model()


class DialogConsumer(AsyncJsonWebsocketConsumer):
    """Handle real-time updates for private dialogs."""

    async def connect(self):
        user = self.scope.get("user")
        if user is None or not user.is_authenticated:
            await self.close()
            return

        username = self.scope.get("url_route", {}).get("kwargs", {}).get("username")
        companion = await self._get_member_by_username(username)
        if companion is None or companion.id == user.id:
            await self.close()
            return

        self.current_user = user
        self.current_user_id = int(user.id)
        self.companion = companion
        self.companion_id = int(companion.id)
        self.group_name = dialog_group_name(self.current_user_id, self.companion_id)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):  # pragma: no cover - network condition
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await super().disconnect(code)

    async def receive_json(self, content, **kwargs):
        action = content.get("action")

        if action == "mark_read":
            ids = content.get("message_ids") or []
            await self._handle_mark_read(ids)

    async def dialog_message(self, event):
        payload = {key: value for key, value in event.items() if key != "type"}
        await self.send_json(payload)

    @database_sync_to_async
    def _get_member_by_username(self, username):
        if not username:
            return None
        return Member.objects.filter(username=username).first()

    async def _handle_mark_read(self, message_ids: List[int]):
        ids = [int(message_id) for message_id in message_ids if str(message_id).isdigit()]
        if not ids:
            return

        updated_ids, read_at = await self._mark_messages_read(ids)
        if not updated_ids:
            return

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "dialog.message",
                "event": "read",
                "message_ids": updated_ids,
                "reader_id": self.current_user_id,
                "read_at": read_at.isoformat(),
                "read_display": timezone.localtime(read_at).strftime("%H:%M"),
            },
        )

    @database_sync_to_async
    def _mark_messages_read(self, message_ids: List[int]):
        now = timezone.now()
        qs = DialogMessage.objects.filter(
            id__in=message_ids,
            recipient_id=self.current_user_id,
            sender_id=self.companion_id,
            read_at__isnull=True,
        )
        updated_ids = list(qs.values_list("id", flat=True))
        if not updated_ids:
            return [], now

        qs.update(read_at=now)
        return updated_ids, now
