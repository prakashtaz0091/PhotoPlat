import json
import hashlib
from channels.generic.websocket import AsyncWebsocketConsumer

def generate_group_name(value: str):
    print("generating group name for ", value)
    return hashlib.sha256(value.encode()).hexdigest()[:100]


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")

        if not self.user.is_authenticated:
            await self.close()
            return

        # user data available here
        self.user_email   = self.user.email
        
        self.group_name = generate_group_name(self.user_email)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def send_notification(self, event):
        print(f"Sending to: {self.channel_name}")
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))