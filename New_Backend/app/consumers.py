import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class MainConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        It will be used to connect user to socket
        """
        req_user = self.scope["user"]
        await self.accept()
        if req_user.is_authenticated:
            self.ride_group = f"ride_share_{req_user.id}"
            await self.channel_layer.group_add(self.ride_group, self.channel_name)
            await self.accept()
        else:
            await self.send(
                {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "error",
                    "message": "unauthorized",
                }
            )
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.ride_group, self.channel_name)

    async def receive(self, text_data):
        if not self.scope["user"].is_authenticated:
            await self.send_error(
                {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "error",
                    "message": "unauthorized",
                }
            )
            return

        data_json = json.loads(text_data)
        self.target_user = self.get_user(user_id=data_json.get("target_user"))
        # TODO: ADd or process logic
        res_json = await self.response_event_creator()
        print(data_json)
        await self.channel_layer.group_send(
            f"ride_share_{self.target_user.id}",
            {"type": "response_request", "res_json": res_json},
        )

    async def response_event_creator(self):
        return {}

    @database_sync_to_async
    def get_user(self, user_id=None, username=None):
        try:
            if username:
                return User.objects.get(username=username)
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        except Exception as e:
            return None
