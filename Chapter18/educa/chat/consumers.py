import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q
from django.utils import timezone

from chat.models import Message
from courses.models import Course


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.id = self.scope["url_route"]["kwargs"]["course_id"]
        self.room_group_name = f"chat_{self.id}"

        if not self.user.is_authenticated or not await self.can_chat():
            await self.close()
            return
        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # check the user is the owner or a student of the course
    async def can_chat(self):
        return await Course.objects.filter(
            Q(owner=self.user) | Q(students=self.user), id=self.id
        ).aexists()

    # persist message to database
    async def persist_message(self, message):
        await Message.objects.acreate(
            user=self.user, course_id=self.id, content=message
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        now = timezone.now()
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.user.username,
                "datetime": now.isoformat(),
            },
        )
        # persist message
        await self.persist_message(message)

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))
