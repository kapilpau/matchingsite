from channels.consumer import AsyncConsumer
from .models import Conversation, Message, Member, Profile
import json
from datetime import datetime

class ChatConsumer(AsyncConsumer):
    convo_id = None
    user = None

    async def websocket_connect(self, event):
        self.user = Member.objects.get(username=self.scope['session']['username'])
        print(event)
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print(event)
        print(self.convo_id)
        msg = json.loads(event['text'])
        print("Msg:")
        try:
            if msg['command'] == 'join':
                self.convo_id = msg['convoID']
                print("Convo id")
                print(type(self.convo_id))
                await self.channel_layer.group_add(self.convo_id, self.channel_name)
                await self.send({"type": "websocket.send", 'text': 'ConnectionSuccessful'})
                return
        except AttributeError:
            print("Exception caught")
        # await self.send({
        #     "type": "websocket.send",
        #     "text": event["text"],
        # })
        await self.send({"type": "websocket.send", 'text': 'MessageReceived'})
        print(self.channel_layer)
        mes = Message.objects.create(sender=self.user, contents=msg['message'], sent_at=datetime.now(), conversation=Conversation.objects.get(id=self.convo_id))
        mes.save()
        await self.channel_layer.group_send(self.convo_id, {
            "type": "websocket.send",
            "text": {
                "msgID": mes.id,
                "sender": mes.sender.profile.name,
                "contents": mes.contents,
                "sent_at": mes.sent_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        })

    async def websocket_disconnect(self, event):
        print(event)
        print("Disconnected")

    async def websocket_send(self, event):
        event['user'] = self.user.profile.name
        text = json.dumps(event)
        await self.send({"type": "websocket.send", "text": text})
        msg = Message.objects.get(id=event['text']['msgID'])
        print(msg.contents)
        print(self.user.profile.name)
        msg.read_by.add(self.user)
        msg.save()
