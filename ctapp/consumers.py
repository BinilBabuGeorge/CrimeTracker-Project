import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, ChatMessage, PanicAlert, PoliceStation, UserInfo, PoliceOfficer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
        self.participant = await self._get_participant()
        if not self.participant:
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self._mark_room_messages_read()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = (data.get("message") or "").strip()
        if not message:
            return

        payload = await self._save_message(message)
        if not payload:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                **payload,
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message_id": event.get("message_id"),
                    "room_id": event.get("room_id"),
                    "message": event.get("message"),
                    "sender_type": event.get("sender_type"),
                    "sender_label": event.get("sender_label"),
                    "created_at": event.get("created_at"),
                    "time_label": event.get("time_label"),
                    "is_read": event.get("is_read", False),
                }
            )
        )

    @database_sync_to_async
    def _get_participant(self):
        session = self.scope.get("session")
        if not session:
            return None

        slogid = session.get("slogid")
        if not slogid:
            return None

        try:
            room = ChatRoom.objects.select_related("user", "police_station").get(pk=self.room_id)
        except ChatRoom.DoesNotExist:
            return None

        if session.get("uname") and room.user.login_id == slogid:
            return {"role": "user", "label": room.user.name, "room_id": room.chat_room_id}

        station = None
        if session.get("stname"):
            station = PoliceStation.objects.filter(login_id=slogid).first()
        elif session.get("pname"):
            officer = PoliceOfficer.objects.select_related("police_station").filter(login_id=slogid).first()
            station = officer.police_station if officer else None

        if station and room.police_station_id == station.police_station_id:
            label = station.station_name or station.place or "Police Station"
            return {"role": "station", "label": label, "room_id": room.chat_room_id}

        return None

    @database_sync_to_async
    def _save_message(self, message: str):
        if not self.participant:
            return None

        room = ChatRoom.objects.get(pk=self.room_id)
        chat_message = ChatMessage.objects.create(
            room=room,
            sender_type=self.participant["role"],
            message=message,
        )
        room.updated_at = timezone.now()
        room.save(update_fields=["updated_at"])
        return {
            "message_id": chat_message.chat_message_id,
            "room_id": room.chat_room_id,
            "message": chat_message.message,
            "sender_type": chat_message.sender_type,
            "sender_label": self.participant["label"],
            "created_at": chat_message.created_at.isoformat(sep=" ", timespec="seconds"),
            "time_label": timezone.localtime(chat_message.created_at).strftime("%I:%M %p"),
            "is_read": False,
        }

    @database_sync_to_async
    def _mark_room_messages_read(self):
        if not self.participant:
            return

        ChatMessage.objects.filter(room_id=self.room_id).exclude(sender_type=self.participant["role"]).filter(is_read=False).update(is_read=True)


class PanicConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # URL patterns:
        # - ws/panic/admin/
        # - ws/panic/station/<station_id>/
        self.station_id = self.scope["url_route"]["kwargs"].get("station_id")
        if self.station_id:
            self.group_name = f"panic_station_{self.station_id}"
        else:
            self.group_name = "panic_admin"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def panic_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))
