import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.core.models import Comment, Tatar


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_' + self.room_name
        self.user = self.scope['user']
        self.MAX_LENGTH = 200

    @staticmethod
    def get_sender_name(user):
        return user.first_name or user.username

    @database_sync_to_async
    def get_word(self):
        return Tatar.objects.get(pk=int(self.room_name))

    @database_sync_to_async
    def get_comments(self, word):
        comment_list = ''
        for c in Comment.objects.filter(word=word):
            comment_list += f'{self.get_sender_name(c.user)}:{c.comment}\n'
        return comment_list

    @database_sync_to_async
    def create_comment(self, message, word):
        Comment.objects.create(user=self.user, comment=message, word=word)

    async def connect(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        word = await self.get_word()
        comments = await self.get_comments(word)
        await self.send(text_data=json.dumps({
            'message': comments
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        if self.user.is_authenticated:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            word = await self.get_word()
            await self.create_comment(message, word)
            if len(message) <= self.MAX_LENGTH:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': f'{self.get_sender_name(self.user)}:{message}'
                    })
        else:
            await self.send(text_data=json.dumps({
                'message': 'Для написания сообщений нужна авторизация'
            }))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))