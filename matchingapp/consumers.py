from channels.consumer import AsyncConsumer
from .models import Conversation, Message, Member, Profile
import json
from datetime import datetime


# Chat Consumer is a class which handles WebSocket events. It has two global variables, the id of the conversation
# that the connection is for and the user who is connected.
class ChatConsumer(AsyncConsumer):
    convo_id = None
    user = None

    # When the connection is established, the user variable is set
    async def websocket_connect(self, event):
        self.user = Member.objects.get(username=self.scope['session']['username'])
        print(event)
        await self.send({
            "type": "websocket.accept",
        })

    # Once the connection is first established, the chat client sends the id of the conversation which sets the convo_id
    # variable and joins the consumer to the conversation group. After that, the messages received are all conversation
    # messages. Every time one is received, it is added to the database, and all of the consumers in the conversation
    # group are alert that there is a new message
    async def websocket_receive(self, event):
        msg = json.loads(event['text'])
        try:
            if msg['command'] == 'join':
                self.convo_id = msg['convoID']
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

    # The disconnect event must be handled but, in this situation, there is nothing that needs to be done on disconnect
    # so it simply prints out that it has disconnected
    async def websocket_disconnect(self, event):
        print(event)
        print("Disconnected")

    # When the receive function alerts the conversation group that there is a new message, it triggers a send event
    # which then sends the message to the connections for the group
    async def websocket_send(self, event):
        event['user'] = self.user.profile.name
        text = json.dumps(event)
        await self.send({"type": "websocket.send", "text": text})
        msg = Message.objects.get(id=event['text']['msgID'])
        msg.read_by.add(self.user)
        msg.save()
