from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterable, List, Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from django.utils.formats import date_format


@dataclass(frozen=True)
class MessagePayload:
    id: int
    sender_id: int
    recipient_id: int
    author: str
    text: str
    created_at: str
    time_display: str
    date: str
    date_display: str
    is_read: bool
    read_at: Optional[str]
    read_display: Optional[str]


def dialog_group_name(user_id: int, companion_id: int) -> str:
    first, second = sorted((int(user_id), int(companion_id)))
    return f"dialog_{first}_{second}"


def _build_date_label(date) -> str:
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)

    if date == today:
        return "Сьогодні"
    if date == yesterday:
        return "Вчора"
    return date_format(date, "j E Y")


def build_message_payload(message) -> MessagePayload:
    created_local = timezone.localtime(message.created_at)
    date = created_local.date()
    read_at = message.read_at
    read_local = timezone.localtime(read_at) if read_at else None

    return MessagePayload(
        id=message.id,
        sender_id=message.sender_id,
        recipient_id=message.recipient_id,
        author=message.sender.get_full_name() or message.sender.username,
        text=message.text,
        created_at=message.created_at.isoformat(),
        time_display=created_local.strftime("%H:%M"),
        date=date.isoformat(),
        date_display=_build_date_label(date),
        is_read=read_at is not None,
        read_at=read_at.isoformat() if read_at else None,
        read_display=read_local.strftime("%H:%M") if read_local else None,
    )


def _send_group_event(group: str, payload: dict) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(group, payload)


def broadcast_new_message(message) -> None:
    payload = build_message_payload(message)
    _send_group_event(
        dialog_group_name(message.sender_id, message.recipient_id),
        {
            "type": "dialog.message",
            "event": "new",
            "message": payload.__dict__,
        },
    )


def broadcast_messages_read(
    reader_id: int,
    companion_id: int,
    message_ids: Iterable[int],
    read_at,
) -> None:
    ids: List[int] = [int(message_id) for message_id in message_ids]
    if not ids:
        return

    read_local = timezone.localtime(read_at)
    _send_group_event(
        dialog_group_name(reader_id, companion_id),
        {
            "type": "dialog.message",
            "event": "read",
            "message_ids": ids,
            "reader_id": int(reader_id),
            "read_at": read_at.isoformat(),
            "read_display": read_local.strftime("%H:%M"),
        },
    )
