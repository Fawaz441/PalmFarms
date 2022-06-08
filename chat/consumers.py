import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from .models import Channel


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.farmer_id = self.scope['url_route']['kwargs']['farmer_id']
        self.customer_id = self.scope['url_route']['kwargs']['customer_id']
        user = self.scope["user"]
        self.room_group_name = 'chat_{0}_{1}'.format(
            self.farmer_id, self.customer_id)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        if str(user.id) in [self.farmer_id, self.customer_id]:
            self.accept()
            old_messages = []
            channel, _ = Channel.objects.get_or_create(
                seller__id=int(self.farmer_id),
                purchaser__id=int(self.customer_id)
            )
            self.channel_obj = channel
            for message in channel.message_set.all():
                old_messages.append({
                    'sender': message.sender.id,
                    'text': message.text,
                    'timestamp': str(message.timestamp)
                })
            self.send(text_data=json.dumps({
                'messages': old_messages
            }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        formatted_message = message.copy()
        formatted_message['timestamp'] = str(timezone.now())
        self.channel_obj.add_message(message['text'], message['sender'])
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': formatted_message
            }
        )

    # Receive message from room group

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
