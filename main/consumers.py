import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import User, Message
from django.db.models import Q
from datetime import datetime
from channels.layers import get_channel_layer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver_id = int(self.scope['url_route']['kwargs']['receiver_id'])
        self.user_id = await sync_to_async(self.get_user_id)()
        # self.user
        if self.user_id > self.receiver_id:
            self.chat_name = 'chat_%s_%s' % (self.user_id, self.receiver_id)
        else:
            self.chat_name = 'chat_%s_%s' % (self.receiver_id, self.user_id)

        await database_sync_to_async(self.update_online_status)('connect')
        await database_sync_to_async(self.update_channel_name)()
        # Join room group
        

        await self.channel_layer.group_add(
                self.chat_name, 
                self.channel_name
            )

        self.channels = await sync_to_async(self.abcd)()
        for channel in self.channels:
            await self.channel_layer.group_add(
                self.chat_name,
                channel['channel']
            )
        # print(type(self.channel_name), '\n', self.channel_name,'\n', self.chat_name)


        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'chat_message',
                'message_type': 'online',
                'message': 'Online',
                'sender_id': self.user_id,
                'receiver_id': self.receiver_id,
                'time': ''
            }
        )


        for channel in self.channels:
            await self.channel_layer.group_discard(
                self.chat_name,
                channel['channel']
            )


        
        

        # print('SELF>CHANNELS:', self.channels, type(self.channels))

        # print("####### CHANNEL NAME::::::::          ", self.channel_name, '+++++++++', self.channel_layer )

        await self.accept()

        # print('@@@@@@@ ', get_channel_layer(), ' @@@@@@@@@@')

        if self.receiver_id != 0:
            messages = await database_sync_to_async(self.get_all_messages)(self.user_id, self.receiver_id)
            await self.send(text_data=json.dumps({
                'message_type': 'all_messages',
                'messages': messages
                }))

            

            online = await database_sync_to_async(self.get_online_status)()
            await self.send(text_data=json.dumps({
                'message_type': 'online',
                'message': online
                }))
        chats = await database_sync_to_async(self.get_all_chats)()
        if chats is not None:
            await self.send(text_data=json.dumps({
                'message_type': 'all_chats',
                'message': chats
                }))

        






        ###################################
        ###################################
    async def disconnect(self, close_code):
        # await self.channel_layer.group_discard(
        #     self.chat_name,
        #     self.channel_name
        # )




        last_seen = await database_sync_to_async(self.update_online_status)('disconnect')

        self.channels = await sync_to_async(self.abcd)()
        for channel in self.channels:
            await self.channel_layer.group_add(
                self.chat_name,
                channel['channel']
            )


        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'chat_message',
                'message_type': 'online',
                'message': str(last_seen),
                'sender_id': 0,# channel['id'],
                'receiver_id': 0,
                'time': ''
            }
        )


        for channel in self.channels:
            await self.channel_layer.group_discard(
                self.chat_name,
                channel['channel']
            )
        # Leave room group


    def get_user_id(self):
        return self.scope['session']['id']

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['message_type']
        message = data['message']
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        # Send message to room group

        if message_type == 'new_message':
            time = await database_sync_to_async(self.create_new_message)(message, sender_id, receiver_id)
        
        else:
            time = ''

        if message_type == 'seen':
            await database_sync_to_async(self.change_unseen_to_seen)(sender_id, receiver_id)
        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'chat_message',
                'message_type': message_type,
                'message': message,
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'time': time,

            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        text_data= {
            'message': message,
            'message_type': event['message_type'],
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
        }
        if event['time'] != '':
            text_data['time'] = event['time'].strftime("%I:%M %p")
        if event.get('seen'):
            text_data['seen'] = event['seen']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(text_data))



    def create_new_message(self, message, sender_id, receiver_id):
        msg = Message(msg=message, author=sender_id, receiver = receiver_id)
        msg.save()
        return msg.time

    def get_all_messages(self, user_id, receiver_id):
        messages = Message.objects.filter(Q(author=user_id)|Q(receiver=user_id), Q(author=receiver_id)|Q(receiver=receiver_id))
        res = []
        if messages.count() > 0:
            for message in messages:
                msg = dict()
                msg['author'] = message.author
                msg['receiver'] = message.receiver
                msg['time'] = message.time.strftime("%I:%M %p")
                msg['msg'] = message.msg
                msg['seen'] = message.seen
                res.append(msg)
        return json.dumps(res)
    def get_all_chats(self):
        user_id = self.user_id
        msgs = Message.objects.filter(Q(author=user_id)|Q(receiver=user_id))
        if len(msgs) > 0:
            users = []
            for msg in msgs:
                if msg.author not in users:
                    users.append(msg.author)
                if msg.receiver not in users:
                    users.append(msg.receiver)
            users.remove(user_id)
            messages = []
            for user in users:
                print(user)
                m = Message.objects.filter(Q(author=user, receiver=user_id)|Q(author=user_id, receiver=user)).last()
                u = User.objects.filter(id=user).first()
                print(m)
                message = {
                    'id': u.id,
                    'username': u.username,
                    'name': u.first_name + ' ' + u.last_name,
                    'last_msg': m.msg,
                    'last_msg_time': m.time.strftime("%I:%M %p"),
                    'last_msg_author': m.author
                }
                messages.append(message)
            return json.dumps(messages)
        else:
            return None
    def get_online_status(self):
        return User.objects.filter(id=self.receiver_id).first().online

    def update_online_status(self, type):
        user = User.objects.filter(id=self.user_id).first()
        # user.online = datetime.now()
        if type == 'connect':
            user.online = 'Online'
        else:
            user.online = datetime.now()

        user.save()
        return user.online

    def abcd(self):
        users = User.objects.all().exclude(id=self.user_id).exclude(id=self.receiver_id)
        res = []
        for user in users:
            res.append({
                'id': user.id,
                'channel': user.channel
                })
        return res

    def update_channel_name(self):
        user = User.objects.filter(id=self.user_id).first()
        user.channel = self.channel_name
        user.save()

    def change_unseen_to_seen(self, s, r):
        msgs = Message.objects.filter(author=s, receiver=r, seen=False)
        for msg in msgs:
            msg.seen = True
            msg.save()


